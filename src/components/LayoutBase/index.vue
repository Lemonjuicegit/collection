<template>
  <div class="layout">
    <aside>
      <div class="resize" :style="{ minWidth:`${minWidth}px` }"></div>
      <div class="line"></div>

      <div class="aside" >
        <div class="aside-header">
          <slot name="aside-header">
          </slot>
        </div>
        <slot name="aside">
        </slot>
      </div>
    </aside>
    <div class="right">
      <div v-if="$slots.header">
        <slot name="header" />
      </div>
      <div v-if="$slots.main">
        <main>
          <slot name="main" />
        </main>
      </div>
      <div v-if="$slots.footer">
        <footer>
          <slot name="footer" />
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  minWidth: {
    type: Number,
    default: 200
  }
})

</script>

<style src="./style.css" scoped></style>