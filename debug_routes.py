import sys
sys.path.append('src')
from src.main import app

print('=== FastAPI Routes ===')
for route in app.routes:
    if hasattr(route, 'path') and hasattr(route, 'methods'):
        print(f'{route.methods} {route.path}')
    elif hasattr(route, 'path'):
        print(f'MOUNT {route.path}')
print('=== End Routes ===')

print('\n=== Router Details ===')
print(f'Total routes: {len(app.routes)}')

# Check specifically for login routes
login_routes = [r for r in app.routes if hasattr(r, 'path') and '/login' in r.path]
print(f'Login routes found: {len(login_routes)}')
for route in login_routes:
    print(f'  {route.methods} {route.path}')

# Check auth router routes
auth_routes = [r for r in app.routes if hasattr(r, 'path') and '/auth' in r.path]
print(f'Auth routes found: {len(auth_routes)}')
for route in auth_routes:
    print(f'  {route.methods} {route.path}')
