import React, { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { ComponentProps, withStreamlitConnection } from "streamlit-component-lib"
import "material-symbols/index.css"

import TreeView from "./TreeView"
import TreeCheckbox from "./TreeCheckbox"


function Router(props: ComponentProps): React.ReactElement {
  switch(props.args["widget"]) {
    case "view":
      return <TreeView {...props} />
    case "checkbox":
      return <TreeCheckbox {...props} />
    default:
      throw new Error(`Unknown widget type: ${props.args["widget"]}`)
  }
}


const ConnectedRouter = withStreamlitConnection(Router)


const rootElement = document.getElementById("root")

if (!rootElement) {
  throw new Error("Root element not found")
}

const root = createRoot(rootElement)

root.render(
  <StrictMode>
    <ConnectedRouter />
  </StrictMode>
)
