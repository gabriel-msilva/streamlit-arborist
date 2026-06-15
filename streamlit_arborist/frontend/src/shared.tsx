import React from "react"
import { NodeApi } from "react-arborist"

import styles from "./arborist.module.css"


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
