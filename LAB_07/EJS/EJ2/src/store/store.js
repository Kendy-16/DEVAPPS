import { legacy_createStore as createStore } from "redux";
import gastosReducer from "./gastosReducer";

const store = createStore(gastosReducer);

export default store;