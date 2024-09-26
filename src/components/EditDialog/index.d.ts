export interface Item {
  label: string
  prop: string
  type: string
  readonly?: boolean
  disabled?: boolean
  width?: number | string
}

export interface Props {
  title: string
  options: Item[]
  formData: Object
  formRules: Array
}