"""
Батч-діагностика всіх модулів holehe.

На відміну від стандартного `holehe email@x.com`, цей скрипт НЕ ховає
помилки за "exists: False" — він показує сиру причину: капча, 403,
timeout, зламаний парсинг чи справді робочий модуль.

Не потребує реальних акаунтів на сайтах — перевіряє лише, чи модуль
технічно живий (чи доходить до нормальної відповіді сервера).

Запуск (з кореня репозиторію holehe, поруч з setup.py):
    pip install -e .
    python3 diagnose_modules.py test.email.check@gmail.com

Якщо email не передати — візьме дефолтний placeholder.
"""

import asyncio
import importlib
import pkgutil
import sys
import time

import httpx


def import_all_modules(package_name="holehe.modules"):
    package = importlib.import_module(package_name)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + "." + name
        try:
            results[full_name] = importlib.import_module(full_name)
        except Exception as e:
            print(f"[!] Не вдалося імпортувати {full_name}: {e}")
        if is_pkg:
            results.update(import_all_modules(full_name))
    return results


def get_module_functions(modules):
    """Повертає список (ім'я_функції, сама_функція)."""
    functions = []
    for module_path, module_obj in modules.items():
        parts = module_path.split(".")
        if len(parts) > 3:
            site = parts[-1]
            func = module_obj.__dict__.get(site)
            if func is not None:
                functions.append((site, func))
    return functions


async def probe_module(name, func, email, client, timeout_s=15):
    """Викликає модуль і класифікує результат по ПРИЧИНІ, а не по exists."""
    out = []
    start = time.time()
    try:
        await asyncio.wait_for(func(email, client, out), timeout=timeout_s)
    except asyncio.TimeoutError:
        return {"name": name, "verdict": "TIMEOUT", "detail": f">{timeout_s}s без відповіді"}
    except httpx.HTTPStatusError as e:
        return {"name": name, "verdict": "HTTP_ERROR", "detail": str(e)}
    except Exception as e:
        # Сюди ж, як правило, потрапляють капча/403/зламаний парсинг JSON,
        # бо самі модулі часто не ловлять ці випадки explicitly.
        return {"name": name, "verdict": "EXCEPTION", "detail": f"{type(e).__name__}: {e}"}

    elapsed = round(time.time() - start, 2)

    if not out:
        return {"name": name, "verdict": "NO_RESULT", "detail": f"модуль відпрацював, але нічого не повернув ({elapsed}s)"}

    result = out[0]

    if result.get("rateLimit"):
        return {"name": name, "verdict": "RATE_LIMIT", "detail": f"модуль сам зафіксував rate limit ({elapsed}s)"}
    if result.get("error"):
        return {"name": name, "verdict": "SWALLOWED_ERROR", "detail": f"модуль зловив власний except і тихо повернув error:True ({elapsed}s)"}

    return {
        "name": name,
        "verdict": "OK",
        "detail": f"exists={result.get('exists')} ({elapsed}s)",
    }


async def main():
    email = sys.argv[1] if len(sys.argv) > 1 else "test.diagnostic.probe@gmail.com"
    print(f"Тестова пошта: {email}\n")

    modules = import_all_modules()
    functions = get_module_functions(modules)
    print(f"Знайдено {len(functions)} модулів.\n")

    async with httpx.AsyncClient(timeout=15) as client:
        # Обмежуємо паралелізм, щоб не влетіти в масовий rate-limit одразу по всіх сайтах
        semaphore = asyncio.Semaphore(10)

        async def bounded_probe(name, func):
            async with semaphore:
                return await probe_module(name, func, email, client)

        results = await asyncio.gather(*[bounded_probe(n, f) for n, f in functions])

    results.sort(key=lambda r: (r["verdict"], r["name"]))

    buckets = {}
    for r in results:
        buckets.setdefault(r["verdict"], []).append(r)

    print("=" * 60)
    print("ПІДСУМОК ПО КАТЕГОРІЯХ")
    print("=" * 60)
    for verdict, items in sorted(buckets.items(), key=lambda x: -len(x[1])):
        print(f"{verdict}: {len(items)}")
    print()

    print("=" * 60)
    print("ДЕТАЛЬНО (згруповано по вердикту)")
    print("=" * 60)
    for verdict, items in buckets.items():
        print(f"\n--- {verdict} ({len(items)}) ---")
        for r in items:
            print(f"  {r['name']:25s} {r['detail']}")

    ok_count = len(buckets.get("OK", []))
    total = len(results)
    print(f"\n{ok_count}/{total} модулів технічно робочі (OK).")
    print("Модулі з OK — кандидати на перевірку логіки (Задача 2, з відомим акаунтом).")
    print("Решта — інфраструктурно мертві, лагодити довше/дорожче (капча, rate limit і т.д.).")


if __name__ == "__main__":
    asyncio.run(main())