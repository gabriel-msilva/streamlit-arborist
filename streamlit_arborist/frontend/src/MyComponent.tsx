import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { NodeApi, NodeRendererProps, Tree } from "react-arborist"
import styles from "./arborist.module.css"

interface State {
  numClicks: number
  isFocused: boolean
}

interface Icons {
  open: string
  closed: string
  leaf: string
}

function get_icon(node: NodeApi<any>, icons: Icons) {
  if (node.isLeaf) {
    return icons.leaf || "🌳";
  }
  return node.isOpen ? icons.open || "🗁" : icons.closed || "🗀";
}

class MyComponent extends StreamlitComponentBase<State> {
  public state = { numClicks: 0, isFocused: false }

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.

    // Streamlit sends us a theme object via props that we can use to ensure
    // that our component has visuals that match the active theme in a
    // streamlit app.
    const { theme } = this.props
    const style: React.CSSProperties = {}

    // Maintain compatibility with older versions of Streamlit that don't send
    // a theme object.
    if (theme) {
      // Use the theme object to style our button border. Alternatively, the
      // theme style is defined in CSS vars.
      const borderStyling = `1px solid ${this.state.isFocused ? theme.primaryColor : "gray"}`
      style.border = borderStyling
      style.outline = borderStyling
    }

    const icons = this.props.args["icons"]
    function Node({ node, style, dragHandle }: NodeRendererProps<any>) {
      return (
        <div
          ref={dragHandle}
          className={styles.node}
          style={style}
        >
          <span
            onClick={(e) => {
              e.stopPropagation();
              node.toggle();
            }}
          >
            {get_icon(node, icons)}
          </span>{" " + node.data.name}
        </div>
      );
    }

    return (
      <Tree
        initialData={this.props.args["data"]}

        // Sizes
        width={this.props.args["width"]}
        height={this.props.args["height"]}
        indent={this.props.args["indent"]}
        rowHeight={this.props.args["row_height"]}
        overscanCount={this.props.args["overscan_count"]}
        paddingTop={this.props.args["padding_top"]}
        paddingBottom={this.props.args["padding_bottom"]}
        padding={this.props.args["padding"]}

        // Config
        childrenAccessor={this.props.args["children_accessor"]}
        idAccessor={this.props.args["id_accessor"]}
        openByDefault={this.props.args["open_by_default"]}
        selectionFollowsFocus={this.props.args["selection_follows_focus"]}
        disableMultiSelection={this.props.args["disable_multi_selection"]}
        // disableEdit={this.props.args["disable_edit"]}
        disableDrag={this.props.args["disable_drag"]}
        disableDrop={this.props.args["disable_drop"]}

        // Selection
        selection={this.props.args["selection"]}
        initialOpenState={this.props.args["initial_open_state"]}

        // Search
        searchTerm={this.props.args["search_term"]}

        // Event handlers
        onActivate={(node) => {
          // if (node.parent) {
          Streamlit.setComponentValue(node.data);
          // }
        }}
      >
        {Node}
      </Tree>
    );
  }

  /** Focus handler for our "Click Me!" button. */
  private _onFocus = (): void => {
    this.setState({ isFocused: true })
  }

  /** Blur handler for our "Click Me!" button. */
  private _onBlur = (): void => {
    this.setState({ isFocused: false })
  }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(MyComponent)
