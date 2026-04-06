from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    # Tempo de espera entre tarefas (5 a 15 segundos)
    wait_time = between(5, 15)

    def on_start(self):
        """Executado quando um usuário virtual inicia"""
        # Exemplo: fazer login
        self.client.post("/login", {
            "username": "test_user",
            "password": ""
        })

    @task
    def index(self):
        """Tarefa principal: acessar página inicial"""
        self.client.get("/")
        self.client.get("/static/assets.js")

    @task
    def about(self):
        """Outra tarefa: acessar página sobre"""
        self.client.get("/about/")