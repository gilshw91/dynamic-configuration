import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export const notifySubmit = () => toast.info("Submitted Sucssefully!");
export const notifyUpdate = () => toast.info("Updated Sucssefully!");
export const notifyDelete = () => toast.info("Deleted Sucssefully!");
export const notifyError = () => toast.error("Operation has failed!");
