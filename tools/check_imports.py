import traceback


def try_import(name):
    print(f"Importing {name}...")
    try:
        __import__(name, fromlist=['*'])
        print(f"OK: {name}\n")
        return True
    except Exception as e:
        print(f"FAILED importing {name}: {e}\n")
        traceback.print_exc()
        return False

modules = [
    'src.data_loader',
    'src.embedding',
    'src.vectorstore',
    'src.search',
    'langchain_community',
    'sentence_transformers',
    'faiss'
]

for m in modules:
    if not try_import(m):
        break

print('Import checks complete')
