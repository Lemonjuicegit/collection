interface DropdownOption {
  label: String
  click: (data: any) => void
}
interface Option {
  name: String | number
  title: String
  dropdownHidden: boolean
  isEditColor: boolean
  dropdownOption: DropdownOption[]
}
