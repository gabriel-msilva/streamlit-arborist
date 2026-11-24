import { FrontendRenderer, FrontendRendererArgs } from "@streamlit/component-v2-lib"
import React, { StrictMode } from "react"
import { createRoot, Root } from "react-dom/client"

import "./material-symbols.css"
import { ComponentProps, getTheme } from "./shared"
import TreeCheckbox from "./TreeCheckbox"
import TreeView from "./TreeView"

function Router(props: ComponentProps): React.ReactElement {
  switch (props.args["widget"]) {
    case "view":
      return <TreeView {...props} />
    case "checkbox":
      return <TreeCheckbox {...props} />
    default:
      throw new Error(`Unknown widget type: ${props.args["widget"]}`)
  }
}

// Streamlit calls the renderer again when the args or the theme change, so reuse
// each component instance's React root.
const reactRoots: WeakMap<FrontendRendererArgs["parentElement"], Root> = new WeakMap()

const renderer: FrontendRenderer<Record<string, unknown>, Record<string, any>> = ({
  data,
  parentElement,
  setStateValue,
}) => {
  const rootElement = parentElement.querySelector(".react-root")

  if (!rootElement) {
    throw new Error("React root element not found")
  }

  let reactRoot = reactRoots.get(parentElement)

  if (!reactRoot) {
    reactRoot = createRoot(rootElement)
    reactRoots.set(parentElement, reactRoot)
  }

  // The theme's CSS custom properties are set on an ancestor of the shadow host.
  const host = parentElement instanceof ShadowRoot ? parentElement.host : parentElement

  reactRoot.render(
    <StrictMode>
      <Router args={data} theme={getTheme(host)} setStateValue={setStateValue} />
    </StrictMode>,
  )

  return () => {
    reactRoots.get(parentElement)?.unmount()
    reactRoots.delete(parentElement)
  }
}

export default renderer
