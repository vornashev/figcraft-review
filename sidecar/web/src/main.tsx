import {createRoot} from "react-dom/client";
import {App} from "./App";
import {connect} from "./actions";
import {exposeForTests} from "./testHooks";
import "@fontsource-variable/golos-text";
import "@fontsource/jetbrains-mono/cyrillic-400.css";
import "@fontsource/jetbrains-mono/latin-400.css";
import "./styles.css";

createRoot(document.getElementById("root")!).render(<App />);
connect();
exposeForTests();
