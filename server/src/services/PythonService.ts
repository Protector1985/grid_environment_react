require("dotenv").config();
import axios from "axios";

class PythonService {
  async sendData(data: any) {
    console.log("DATA!!")
    try {
      const response = await axios.post(
        process.env.FLASK_SERVER_URL as string,
        {data:data},
      );
      
      return {
        success: true,
        data: response.data,
      };
    } catch (err) {
      return {
        success: false,
        data: err,
      };
    }
  }
}

export default PythonService;
