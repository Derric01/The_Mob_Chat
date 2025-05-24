from app import app, socketio

if  __name__ == "__main__":
 socketio.run(app)

 #Guincorn is a Python WSGI HTTP server for UNIX. It serves web applications in a concurrent, pre-fork worker model.
 # It is a popular choice for deploying Flask applications in production environments.