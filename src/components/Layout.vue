<template>
    <div class="layout">
        <aside>
            <div class="resize"></div>
            <div class="line"></div>
            <div class="aside">
                <slot name="aside">
                </slot>
            </div>
        </aside>
        <div class="right">
            <slot name="header">
            </slot>
            <main>
                <slot name="main">
                </slot>
            </main>
            <footer>
                <slot name="footer">
                </slot>
            </footer>
        </div>
    </div>
</template>

<script setup>

</script>

<style scoped>
.layout {
    width: 100%;
    height: 100vh;
    display: flex;
}

aside {
    position: relative;
    min-width: 200px;
    height: 100%;
}

.aside {
    position: absolute;
    top: 0;
    left: 0;
    width: calc(100% - 25px);
    height: 100%;
    padding: 10px 10px 10px 10px;
}

.line {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    width: 2px;
    height: 100%;
    background-color: #c8c9cc;
}

.right {
    display: flex;
    justify-content: space-between;
    flex-direction: column;
    flex: 1;
    height: 100%;
    min-width: 200px;
}

main {
    height: calc(100% - 50px);
    margin: 10px 10px 10px 10px;
    border-radius: 5px;
    overflow-y: scroll
}

footer {
    width: 100%;
    height: 50px;
}

.resize {
    min-width: 200px;
    height: 10px;
    resize: horizontal;
    overflow: scroll;
    transform: scaleY(200);
    opacity: 0;

    &:active+.line {
        width: 4px;
        background-color: #c6e2ff;
        box-shadow: 0px 0px 5px 2px #dedfe0;
    }
}
</style>