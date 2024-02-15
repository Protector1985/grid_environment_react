import express, { Router, Request, Response } from "express";
import PythonService from "../services/PythonService";
import multer, { Multer } from "multer";
import FormData from "form-data";


class PythonController extends PythonService {
  private basepath: string = "/ai";
  public router: Router = express.Router();
  private uploadEngine: Multer = multer({ storage: multer.memoryStorage() }); //storage engine - stores in memory

  constructor() {
    super();
    this.initRoutes();
  }

  initRoutes() {
    this.router.post(
      this.basepath + "/startTraining",
      this.submitToFlask,
    );
  }

  //BELOW HAS TO BE ERROR FUNCTION otherwise this.sendData is undefined due to context
  submitToFlask = async (req: Request, res: Response) => {
    const resp = await this.sendData(req.body);
    res.send(resp)
  };
}

export default PythonController;
