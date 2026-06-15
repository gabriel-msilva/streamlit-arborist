import clsx from "clsx"
import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react"
import { NodeApi, NodeRendererProps, Tree, TreeApi } from "react-arborist"
import {
  ComponentProps,
  Streamlit,
  withStreamlitConnection,
} from "streamlit-component-lib"

import styles from "./arborist.module.css"


interface Icons {
  open: string
  closed: string
  leaf: string
}


interface TreeIndex {
  parentOf: Map<string, string | null>
  childrenOf: Map<string, string[]>
  allIds: string[]
}


function buildTreeIndex(
  data: any[] | undefined,
  childrenAccessor: string,
  idAccessor: string
): TreeIndex {
  const parentOf = new Map<string, string | null>()
  const childrenOf = new Map<string, string[]>()
  const allIds: string[] = []

  const visit = (nodes: any[] | undefined, parent: string | null) => {
    if (!nodes) return

    for (const node of nodes) {
      const id = String(node[idAccessor])
      if (parentOf.has(id)) {
        console.warn(`streamlit-arborist: duplicate node id "${id}"`)
      }

      parentOf.set(id, parent)
      allIds.push(id)

      const children = node[childrenAccessor]
      if (Array.isArray(children) && children.length > 0) {
        childrenOf.set(id, children.map((c: any) => String(c[idAccessor])))
        visit(children, id)
      } else {
        childrenOf.set(id, [])
      }
    }
  }

  visit(data, null)

  return { parentOf, childrenOf, allIds }
}


// Walk a subtree in data order and apply a mutation to every children (including the root).
// Operates over the data index, not NodeApi, so it works for collapsed/off-screen nodes.
function cascadeDown(
  rootId: string,
  willCheck: boolean,
  index: TreeIndex,
  checked: Set<string>,
  indeterminate: Set<string>
) {
  const stack = [rootId]

  while (stack.length > 0) {
    const id = stack.pop()!

    if (willCheck) {
      checked.add(id)
    } else {
      checked.delete(id)
    }

    indeterminate.delete(id)

    const children = index.childrenOf.get(id) || []
    for (const k of children) stack.push(k)
  }
}


function cascadeUp(
  startId: string,
  index: TreeIndex,
  checked: Set<string>,
  indeterminate: Set<string>
) {
  let current = index.parentOf.get(startId) ?? null

  while (current !== null) {
    const children = index.childrenOf.get(current) || []

    let allChecked = children.length > 0
    let anyChecked = false
    let anyIndeterminate = false

    for (const k of children) {
      if (checked.has(k)) {
        anyChecked = true
      } else {
        allChecked = false
      }

      if (indeterminate.has(k)) anyIndeterminate = true
    }

    if (allChecked) {
      checked.add(current)
      indeterminate.delete(current)
    } else if (!anyChecked && !anyIndeterminate) {
      checked.delete(current)
      indeterminate.delete(current)
    } else {
      checked.delete(current)
      indeterminate.add(current)
    }

    current = index.parentOf.get(current) ?? null
  }
}


function seedState(
  seedIds: string[],
  index: TreeIndex
): { checked: Set<string>; indeterminate: Set<string> } {
  const checked = new Set<string>()
  const indeterminate = new Set<string>()

  for (const id of seedIds) {
    if (index.parentOf.has(id)) cascadeDown(id, true, index, checked, indeterminate)
  }

  for (const id of seedIds) {
    if (index.parentOf.has(id)) cascadeUp(id, index, checked, indeterminate)
  }

  return { checked, indeterminate }
}


function renderIcon(node: NodeApi<any>, icons: Icons) {
  let icon: string

  if (node.isLeaf) {
    icon = icons.leaf
  } else {
    icon = node.isOpen ? icons.open : icons.closed
  }

  const materialMatch = icon?.match(/^:material\/(.+):$/)
  if (materialMatch) {
    return (
      <span className={`material-symbols-rounded ${styles.icon}`}>
        {materialMatch[1]}
      </span>
    )
  }

  return <span className={styles.icon}>{icon}</span>
}


function TreeView(props: ComponentProps): React.ReactElement {
  const args = props.args
  const themeProp = props.theme

  const mode: "single" | "checkbox" = args["mode"] === "checkbox" ? "checkbox" : "single"
  const data = args["data"]
  const icons = args["icons"] as Icons
  const childrenAccessor = args["children_accessor"]
  const idAccessor = args["id_accessor"]
  const seed = args["checked"] as string[] | null | undefined
  const selectInternalNodes = args["select_internal_nodes"] === true

  // This is a workaround for the fact that Streamlit's `props.theme` object does not
  // contain all color properties, such as `darkenedBgMix15` and `darkenedBgMix25`.
  const theme = useMemo(
    () => (themeProp ? JSON.parse(JSON.stringify(themeProp)) : {}),
    [themeProp]
  )

  const index = useMemo(
    () => buildTreeIndex(data, childrenAccessor, idAccessor),
    [data, childrenAccessor, idAccessor]
  )

  const [checked, setChecked] = useState<Set<string>>(() => new Set())
  const [indeterminate, setIndeterminate] = useState<Set<string>>(() => new Set())

  // Seed initial state once per index (i.e. once per `data` change).
  // The `checked` prop is treated as initial-only:
  // re-sends from Streamlit do not overwrite frontend state mid-session.
  const seededRef = useRef<TreeIndex | null>(null)
  useEffect(() => {
    if (seededRef.current === index) return

    seededRef.current = index
    const { checked: c, indeterminate: i } = seedState(seed ?? [], index)

    setChecked(c)
    setIndeterminate(i)

    if (mode === "checkbox") {
      Streamlit.setComponentValue(Array.from(c).sort())
    }
  }, [index])

  const toggleNode = useCallback(
    (id: string) => {
      const draftChecked = new Set(checked)
      const draftIndet = new Set(indeterminate)
      const willCheck = !draftChecked.has(id)

      cascadeDown(id, willCheck, index, draftChecked, draftIndet)
      cascadeUp(id, index, draftChecked, draftIndet)
      setChecked(draftChecked)
      setIndeterminate(draftIndet)

      Streamlit.setComponentValue(Array.from(draftChecked).sort())
    },
    [checked, indeterminate, index]
  )

  const renderNode = (rendererProps: NodeRendererProps<any>) => (
    <NodeRow
      rendererProps={rendererProps}
      mode={mode}
      theme={theme}
      icons={icons}
      selectInternalNodes={selectInternalNodes}
      isChecked={checked.has(rendererProps.node.id)}
      isIndeterminate={indeterminate.has(rendererProps.node.id)}
      onToggle={toggleNode}
    />
  )

  const treeRef = useRef<TreeApi<any> | undefined>(undefined)

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (mode !== "checkbox") return
    if (e.key !== " ") return

    const focused = treeRef.current?.focusedNode
    if (!focused) return

    e.preventDefault()
    e.stopPropagation()
    toggleNode(focused.id)
  }

  return (
    <div onKeyDown={handleKeyDown}>
      <Tree
        ref={treeRef}
        initialData={data}
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
        childrenAccessor={childrenAccessor}
        idAccessor={idAccessor}
        openByDefault={args["open_by_default"]}
        disableMultiSelection={true}
        disableEdit={true}
        disableDrag={true}
        disableDrop={true}
        // Event handlers
        onSelect={(nodes) => {
          if (mode === "checkbox") return
          if (nodes.length !== 0) {
            Streamlit.setComponentValue(nodes[0].data)
          }
        }}
        // Selection
        selection={mode === "checkbox" ? undefined : args["selection"]}
        // Open State
        initialOpenState={args["initial_open_state"]}
        // Search
        searchTerm={args["search_term"]}
      >
        {renderNode}
      </Tree>
    </div>
  )
}


interface NodeRowProps {
  rendererProps: NodeRendererProps<any>
  mode: "single" | "checkbox"
  theme: any
  icons: Icons
  selectInternalNodes: boolean
  isChecked: boolean
  isIndeterminate: boolean
  onToggle: (id: string) => void
}


function NodeRow({
  rendererProps,
  mode,
  theme,
  icons,
  selectInternalNodes,
  isChecked,
  isIndeterminate,
  onToggle,
}: NodeRowProps) {
  const { node, style, dragHandle } = rendererProps
  const [isHover, setHover] = useState(false)

  const hoverStyle: React.CSSProperties = { backgroundColor: theme.darkenedBgMix15 }
  const selectedStyle: React.CSSProperties =
    mode === "checkbox"
      ? { backgroundColor: theme.darkenedBgMix25 }
      : { backgroundColor: theme.darkenedBgMix25, fontWeight: "bold" }

  const handleRowClick = (e: React.MouseEvent) => {
    if (mode === "checkbox") {
      // Click toggles the check (cascade for internals). We DON'T stop propagation here:
      // let `react-arborist` handle row focus so Space can target it from the keyboard handler.
      // The chevron and checkbox each have their own handlers with `stopPropagation()` to
      // avoid double-firing.

      // `e.detail` is the click count for this gesture:
      //   1 = single,
      //   2 = the 2nd click of a double-click.
      // Skipping `detail === 2` means the toggle from click 1 stands and the
      // double-click handler can add open/close on top of it.
      // (net effect: double-click toggles check AND open/close)
      if (e.detail === 2) return
      onToggle(node.id)
      return
    }
    if (node.isInternal && !selectInternalNodes) {
      e.stopPropagation()
      node.toggle()
    }
  }

  const handleRowDoubleClick = (e: React.MouseEvent) => {
    if (mode === "checkbox" && node.isInternal) {
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

  const chevronElement =
    mode === "checkbox" ? (
      node.isInternal ? (
        <span
          className={styles.chevron}
          onClick={(e) => {
            e.stopPropagation()
            node.toggle()
          }}
          role="button"
          aria-label={node.isOpen ? "Collapse" : "Expand"}
          data-chevron-id={node.id}
          data-open={node.isOpen}
        >
          <span className="material-symbols-rounded">chevron_forward</span>
        </span>
      ) : (
        <span className={styles.chevronSpacer} aria-hidden="true" />
      )
    ) : null

  const iconElement =
    mode !== "checkbox" && node.isInternal && selectInternalNodes ? (
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
    mode !== "checkbox" && node.isInternal && selectInternalNodes ? (
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

  const checkboxElement =
    mode === "checkbox" ? (
      <CheckboxCell
        nodeId={node.id}
        checked={isChecked}
        indeterminate={isIndeterminate}
        onToggle={() => onToggle(node.id)}
      />
    ) : null

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
      onDoubleClick={handleRowDoubleClick}
    >
      {chevronElement}
      {checkboxElement}
      {iconElement}
      {labelElement}
    </div>
  )
}


function CheckboxCell({
  nodeId,
  checked,
  indeterminate,
  onToggle,
}: {
  nodeId: string
  checked: boolean
  indeterminate: boolean
  onToggle: () => void
}) {
  const ref = useRef<HTMLInputElement>(null)
  useEffect(() => {
    if (ref.current) {
      ref.current.indeterminate = indeterminate
    }
  }, [indeterminate, checked])

  return (
    <span className={styles.checkboxWrapper}>
      <input
        ref={ref}
        type="checkbox"
        className={styles.checkbox}
        data-node-id={nodeId}
        checked={checked}
        onChange={onToggle}
        onClick={(e) => e.stopPropagation()}
        tabIndex={-1}
        aria-label={`Toggle ${nodeId}`}
      />
      {(checked || indeterminate) && (
        <svg className={styles.checkmark} viewBox="0 0 10 8" aria-hidden="true">
          {indeterminate ? (
            <line x1="1" y1="4" x2="9" y2="4" />
          ) : (
            <polyline points="1 4 4 7 9 1" />
          )}
        </svg>
      )}
    </span>
  )
}


export default withStreamlitConnection(TreeView)
