import express, { Application } from "express";
import PythonService from "./services/PythonService";
import PythonController from "./controllers/PythonController";

class App {
  private app: Application = express();
  private port: string;

  constructor(props: {
    port: string;
    middlewares: any[];
    services: Array<PythonService>;
    controllers: Array<PythonController>;
  }) {
    this.port = props.port;
    this.initMiddlewares(props.middlewares);
    this.routes(props.controllers);
  }

  initMiddlewares(middlewares: any[]) {
    middlewares.forEach((middleware: any) => {
      this.app.use(middleware);
    });
    console.log("Middlewares initialized");
  }

  routes(controllers: any[]) {
    controllers.forEach((controller) => {
      this.app.use("/v1", controller.router);
    });
    console.log("V1 routes initialized");
  }

  startServer() {
    this.app.listen(this.port, () => {
      console.log(`Server listening on port ${this.port} `);
    });
  }
}

export default App;
