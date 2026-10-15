import React, { useMemo } from "react"
import { NodeApi } from "react-arborist"

import styles from "./arborist.module.css"

// Streamlit resends args with new object identities (same contents) when the
// iframe resizes, e.g. toggling the sidebar in wide layout. Keep the previous
// reference while the contents are unchanged so memos and effects don't re-run.
export function useStableValue<T>(value: T): T {
  const key = useMemo(() => JSON.stringify(value), [value])
  // eslint-disable-next-line react-hooks/exhaustive-deps
  return useMemo(() => value, [key])
}

export interface Icons {
  open: string
  closed: string
  leaf: string
}

export function renderIcon(node: NodeApi<any>, icons: Icons) {
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
