import sys
sys.path.append('src')
from src.config import settings

print('=== Excluded Paths Configuration ===')
print('Raw auth_excluded_paths:', repr(settings.auth_excluded_paths))
print('Parsed excluded_paths_list:', settings.excluded_paths_list)
print()

# Test path matching logic
test_paths = ['/login', '/register', '/api/v1/auth/login', '/api/v1/auth/register', '/health', '/', '/docs']
print('=== Path Matching Test ===')
for path in test_paths:
    is_excluded = any(path.startswith(excluded) for excluded in settings.excluded_paths_list)
    print(f'{path:<25} -> Excluded: {is_excluded}')

