from auto_everything.disk import Store
store = Store("test", use_sql=False)

store.set("hi", {"you":2})
store.set("ok", {"fuck":2})
print(store.get("hi"))
print(store.get_items())
store.delete("hi")
print(store.get_items())
store.reset()
print(store.get_items())
