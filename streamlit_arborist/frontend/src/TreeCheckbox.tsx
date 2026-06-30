import clsx from "clsx"
import React, { useCallback, useEffect, useMemo, useRef, useState } from "react"
import { NodeRendererProps, Tree, TreeApi } from "react-arborist"
import { ComponentProps, Streamlit } from "streamlit-component-lib"

import { Icons, renderIcon } from "./shared"
import styles from "./arborist.module.css"

function TreeCheckbox(props: ComponentProps): React.ReactElement {
  const args = props.args
  const themeProp = props.theme

  const data = args["data"]
  const icons = args["icons"] as Icons
  const childrenAccessor = args["children_accessor"]
  const idAccessor = args["id_accessor"]
  const seed = args["checked"] as string[]

  // Workaround: Streamlit's `props.theme` object does not contain all color
  // properties (e.g. `darkenedBgMix15`, `darkenedBgMix25`). The deep clone
  // also stabilises the memo across re-renders.
  const theme = useMemo(
    () => (themeProp ? JSON.parse(JSON.stringify(themeProp)) : {}),
    [themeProp],
  )

  const index = useMemo(
    () => buildTreeIndex(data, childrenAccessor, idAccessor),
    [data, childrenAccessor, idAccessor],
  )

  const [checked, setChecked] = useState<Set<string>>(() => new Set())
  const [indeterminate, setIndeterminate] = useState<Set<string>>(() => new Set())

  // Seed initial state once per index (i.e. once per `data` change).
  // The `checked` prop is treated as initial-only: re-sends from Streamlit do not
  // overwrite frontend state mid-session.
  const seededRef = useRef<TreeIndex | null>(null)
  useEffect(() => {
    if (seededRef.current === index) return

    seededRef.current = index
    const { checked: c, indeterminate: i } = seedState(seed, index)

    setChecked(c)
    setIndeterminate(i)

    Streamlit.setComponentValue(Array.from(c).sort())
    // eslint-disable-next-line react-hooks/exhaustive-deps
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
    [checked, indeterminate, index],
  )

  const treeRef = useRef<TreeApi<any> | undefined>(undefined)

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key !== " ") return

    const focused = treeRef.current?.focusedNode
    if (!focused) return

    e.preventDefault()
    e.stopPropagation()
    toggleNode(focused.id)
  }

  const renderNode = (rendererProps: NodeRendererProps<any>) => (
    <NodeRow
      rendererProps={rendererProps}
      icons={icons}
      isChecked={checked.has(rendererProps.node.id)}
      isIndeterminate={indeterminate.has(rendererProps.node.id)}
      onToggle={toggleNode}
    />
  )

  // Hover/selected colors are applied in CSS; expose the theme values as custom
  // properties here so the row stylesheet can read them (see arborist.module.css).
  const themeVars = {
    "--arborist-hover-bg": theme.darkenedBgMix15,
    "--arborist-selected-bg": theme.darkenedBgMix25,
  } as React.CSSProperties

  return (
    <div onKeyDown={handleKeyDown} style={themeVars}>
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

interface TreeIndex {
  parentOf: Map<string, string | null>
  childrenOf: Map<string, string[]>
  allIds: string[]
}

function buildTreeIndex(
  data: any[] | undefined,
  childrenAccessor: string,
  idAccessor: string,
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
        childrenOf.set(
          id,
          children.map((c: any) => String(c[idAccessor])),
        )
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
  indeterminate: Set<string>,
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
  indeterminate: Set<string>,
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
  index: TreeIndex,
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

interface NodeRowProps {
  rendererProps: NodeRendererProps<any>
  icons: Icons
  isChecked: boolean
  isIndeterminate: boolean
  onToggle: (id: string) => void
}

function NodeRow({
  rendererProps,
  icons,
  isChecked,
  isIndeterminate,
  onToggle,
}: NodeRowProps) {
  const { node, style, dragHandle } = rendererProps

  const handleRowClick = (e: React.MouseEvent) => {
    // Click toggles the check (cascade for internals). We DON'T stop propagation here:
    // let `react-arborist` handle row focus so Space can target it from the keyboard handler.
    // The chevron and checkbox each have their own handlers with `stopPropagation()` to
    // avoid double-firing.
    //
    // `e.detail` is the click count for this gesture:
    //   1 = single,
    //   2 = the 2nd click of a double-click.
    // Skipping `detail === 2` means the toggle from click 1 stands and the
    // double-click handler can add open/close on top of it.
    // (net effect: double-click toggles check AND open/close)
    if (e.detail === 2) return
    onToggle(node.id)
  }

  const handleRowDoubleClick = (e: React.MouseEvent) => {
    if (node.isInternal) {
      e.stopPropagation()
      node.toggle()
    }
  }

  const chevronElement = node.isInternal ? (
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

  return (
    <div
      className={clsx(styles.node, node.state)}
      ref={dragHandle}
      style={style}
      onClick={handleRowClick}
      onDoubleClick={handleRowDoubleClick}
    >
      {chevronElement}
      <CheckboxCell
        nodeId={node.id}
        checked={isChecked}
        indeterminate={isIndeterminate}
        onToggle={() => onToggle(node.id)}
      />
      {renderIcon(node, icons)}
      {node.data.name || node.data.id}
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

export default TreeCheckbox
