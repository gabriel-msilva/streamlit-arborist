import clsx from "clsx"
import React, { ReactNode, useState, useMemo } from "react"
import { NodeApi, NodeRendererProps, Tree } from "react-arborist"
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"

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


class TreeView extends StreamlitComponentBase<State> {
  public state = { numClicks: 0, isFocused: false }

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible via `this.props.args`.

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

    return (
      <Tree
        initialData={this.props.args["data"]}

        // Sizes
        rowHeight={this.props.args["row_height"]}
        overscanCount={this.props.args["overscan_count"]}
        width={this.props.args["width"]}
        height={this.props.args["height"]}
        indent={this.props.args["indent"]}
        paddingTop={this.props.args["padding_top"]}
        paddingBottom={this.props.args["padding_bottom"]}
        padding={this.props.args["padding"]}

        // Config
        childrenAccessor={this.props.args["children_accessor"]}
        idAccessor={this.props.args["id_accessor"]}
        openByDefault={this.props.args["open_by_default"]}
        disableMultiSelection={this.props.args["disable_multi_selection"]}
        disableEdit={true}
        disableDrag={true}
        disableDrop={true}

        // Event handlers
        onSelect={(nodes) => {
           const selectedData = nodes.map(node => node.data);
           Streamlit.setComponentValue(selectedData)
        }}

        // Selection
        selection={this.props.args["selection"]}

        // Open State
        initialOpenState={this.props.args["initial_open_state"]}

        // Search
        searchTerm={this.props.args["search_term"]}
      >
        {this.Node}
      </Tree>
    );
  }

  private Node = ({ node, style, dragHandle }: NodeRendererProps<any>) => {
    const [isHover, setHover] = useState(false);

    // This is a workaround for the fact that Streamlit's `props.theme` object does not
    // contain all color properties, such as `darkenedBgMix15` and `darkenedBgMix25`.
    const theme = useMemo(
      () => JSON.parse(JSON.stringify(this.props.theme)), [this.props.theme]
    );

    const hoverStyle: React.CSSProperties = { backgroundColor: theme.darkenedBgMix15 };
    const selectedStyle: React.CSSProperties = {
      backgroundColor: theme.darkenedBgMix25,
      fontWeight: "bold"
    };

    return (
      <div
        className={clsx(styles.node, node.state)}
        style={
          {
            ...style,
            ...(isHover ? hoverStyle : {}),
            ...(node.isSelected ? selectedStyle : {})
          }
        }
        ref={dragHandle}
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
      >
        <span
          className={styles.icon}
          onClick={(e) => { e.stopPropagation(); node.toggle(); }}
        >
          {this.getIcon(node)}
        </span>
        {node.data.name}
      </div>
    );
  }

  private getIcon(node: NodeApi<any>) {
    let icons: Icons = this.props.args["icons"] as Icons;

    if (node.isLeaf) {
      return icons.leaf;
    }

    return node.isOpen ? icons.open : icons.closed;
  }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(TreeView)
