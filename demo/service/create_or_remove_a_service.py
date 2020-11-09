from auto_everything.base import Super

s = Super(username="yingshaoxo")

#s.start_service("test", "additional_script_for_creating_a_service.py")
#s.stop_service("test")
s.service("test", "additional_script_for_creating_a_service.py")
