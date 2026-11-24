import { FrontendRendererArgs } from "@streamlit/component-v2-lib"
import { darken, getLuminance, lighten, mix, transparentize } from "color2k"
import { useMemo } from "react"
import { NodeApi } from "react-arborist"

import styles from "./arborist.module.css"

export interface ComponentProps {
  args: Record<string, any>
  theme: Theme
  setStateValue: FrontendRendererArgs["setStateValue"]
}

// Theme colors that Streamlit derives but doesn't expose to v2 components.
export interface Theme {
  darkenedBgMix15: string
  darkenedBgMix25: string
}

// Same derivation as `computeDerivedColors` in Streamlit's `getColors.ts`.
export function getTheme(element: Element): Theme {
  const style = getComputedStyle(element)
  const bgColor = style.getPropertyValue("--st-background-color")
  const secondaryBg = style.getPropertyValue("--st-secondary-background-color")

  const bgMix = mix(bgColor, secondaryBg, 0.5)
  const darkenedBgMix100 =
    getLuminance(bgColor) > 0.5 ? darken(bgMix, 0.3) : lighten(bgMix, 0.6)

  return {
    darkenedBgMix15: transparentize(darkenedBgMix100, 0.85),
    darkenedBgMix25: transparentize(darkenedBgMix100, 0.75),
  }
}

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
