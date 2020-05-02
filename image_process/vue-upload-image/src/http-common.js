import axios from "axios";

export default axios.create({
  baseURL: "http://52.151.241.182",
  headers: {
    "Content-type": "application/json"
  }
});
