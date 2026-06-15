import clsx from "clsx"
import React, { useMemo, useState } from "react"
import { NodeRendererProps, Tree } from "react-arborist"
import { ComponentProps, Streamlit } from "streamlit-component-lib"

import { Icons, renderIcon } from "./shared"
import styles from "./arborist.module.css"


function TreeView(props: ComponentProps): React.ReactElement {
  const args = props.args
  const themeProp = props.theme

  // Workaround: Streamlit's `props.theme` object does not contain all color
  // properties (e.g. `darkenedBgMix15`, `darkenedBgMix25`). The deep clone
  // also stabilises the memo across re-renders.
  const theme = useMemo(
    () => (themeProp ? JSON.parse(JSON.stringify(themeProp)) : {}),
    [themeProp]
  )

  const icons = args["icons"] as Icons
  const renderNode = (rendererProps: NodeRendererProps<any>) => (
    <NodeRow
      rendererProps={rendererProps}
      theme={theme}
      icons={icons}
      selectInternalNodes={args["select_internal_nodes"]}
    />
  )

  return (
    <Tree
      initialData={args["data"]}
      // Sizes
      rowHeight={args["row_height"]}
      overscanCount={args["overscan_count"]}
      width={args["width"]}
      height={args["height"]}
      indent={args["indent"]}
      paddingTop={args["padding_top"]}
      paddingBottom={args["padding_bottom"]}
      padding={args["padding"]}
      // Config
      childrenAccessor={args["children_accessor"]}
      idAccessor={args["id_accessor"]}
      openByDefault={args["open_by_default"]}
      disableMultiSelection={true}
      disableEdit={true}
      disableDrag={true}
      disableDrop={true}
      // Event handlers
      onSelect={(nodes) => {
        if (nodes.length !== 0) {
          Streamlit.setComponentValue(nodes[0].data)
        }
      }}
      // Selection
      selection={args["selection"]}
      // Open State
      initialOpenState={args["initial_open_state"]}
      // Search
      searchTerm={args["search_term"]}
    >
      {renderNode}
    </Tree>
  )
}


interface NodeRowProps {
  rendererProps: NodeRendererProps<any>
  theme: any
  icons: Icons
  selectInternalNodes: boolean
}


function NodeRow({
  rendererProps,
  theme,
  icons,
  selectInternalNodes,
}: NodeRowProps) {
  const { node, style, dragHandle } = rendererProps
  const [isHover, setHover] = useState(false)

  const hoverStyle: React.CSSProperties = { backgroundColor: theme.darkenedBgMix15 }
  const selectedStyle: React.CSSProperties = {
    backgroundColor: theme.darkenedBgMix25,
    fontWeight: "bold",
  }

  const handleRowClick = (e: React.MouseEvent) => {
    if (node.isInternal && !selectInternalNodes) {
      e.stopPropagation()
      node.toggle()
    }
  }

  const handleIconClick = (e: React.MouseEvent) => {
    if (node.isInternal) {
      e.stopPropagation()
      node.toggle()
    }
  }

  const iconElement =
    node.isInternal && selectInternalNodes ? (
      <span
        className={styles.iconClickTarget}
        onClick={handleIconClick}
        role="button"
        aria-label={node.isOpen ? "Collapse" : "Expand"}
      >
        {renderIcon(node, icons)}
      </span>
    ) : (
      renderIcon(node, icons)
    )

  const labelElement =
    node.isInternal && selectInternalNodes ? (
      <span
        className={styles.label}
        onDoubleClick={(e) => {
          e.stopPropagation()
          node.toggle()
        }}
      >
        {node.data.name || node.data.id}
      </span>
    ) : (
      node.data.name || node.data.id
    )

  return (
    <div
      className={clsx(styles.node, node.state)}
      ref={dragHandle}
      style={{
        ...style,
        ...(isHover ? hoverStyle : {}),
        ...(node.isSelected ? selectedStyle : {}),
      }}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      onClick={handleRowClick}
    >
      {iconElement}
      {labelElement}
    </div>
  )
}


export default TreeView
