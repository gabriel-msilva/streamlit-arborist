import { FrontendRendererArgs } from "@streamlit/component-v2-lib"
import { useMemo } from "react"
import { NodeApi } from "react-arborist"

import styles from "./arborist.module.css"

export interface ComponentProps {
  args: Record<string, any>
  setStateValue: FrontendRendererArgs["setStateValue"]
}

// Streamlit's `darkenedBgMix15` and `darkenedBgMix25` theme colors, which
// aren't exposed to v2 components.
export const HOVER_COLOR = "rgba(151, 166, 195, 0.15)"
export const SELECTED_COLOR = "rgba(151, 166, 195, 0.25)"

// Streamlit parses all args again when any of them changes, so unchanged values
// get new object identities. Keep the previous reference while the contents are
// unchanged so memos and effects don't re-run.
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
