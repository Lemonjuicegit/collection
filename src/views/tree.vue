<div class="block">
          <el-tree
            :data="data"
            node-key="id"
            default-expand-all
            :expand-on-click-node="false"
            @node-click="nodeclick"
            @node-drag-start="handleDragStart"
            @node-drag-enter="handleDragEnter"
            @node-drag-leave="handleDragLeave"
            @node-drag-over="handleDragOver"
            @node-drag-end="handleDragEnd"
            @node-drop="handleDrop"
            draggable
            :allow-drop="allowDrop"
            :allow-drag="allowDrag"
          >
            <span class="custom-tree-node" slot-scope="{ node, data }">
              <!-- 如果是编辑状态 -->
              <template v-if="data.isEdit == 1">
                <el-input
                  ref="input"
                  @blur="() => submitEdit(node, data)"
                  v-model="newApiGroupName"
                  style="height:20px line-height:20px"
                ></el-input>
              </template>
              <!-- 如果不是编辑状态 -->
              <span v-else v-text="data.apiGroupName"></span>
              <span class="m-l1">
                <el-button
                  v-if="data.id != 1"
                  type="text"
                  size="mini"
                  @click="() => edit(node, data)"
                >
                  <i class="el-icon-edit" title="编辑"></i>
                </el-button>
                <el-button
                  type="text"
                  size="mini"
                  @click="() => append(node, data)"
                >
                  <i class="el-icon-plus" title="新增"></i>
                </el-button>
                <el-button
                  v-if="data.id != 1"
                  type="text"
                  size="mini"
                  @click="() => remove(node, data)"
                >
                  <i class="el-icon-delete" title="删除"></i>
                </el-button>
              </span>
            </span>
          </el-tree>
        </div>


  data() {
    return {
      data: [{id:1, apiGroupName: 'eltree分类', children: []}],
      newApiGroupName: "",
      defaultProps: {
        children: "children",
        apiGroupName: "apiGroupName",
      },
    };
  },


    handleDragStart(node, ev) {
      console.log("drag start", node.data.apiGroupName);
    },
    handleDragEnter(draggingNode, dropNode, ev) {
      console.log("tree drag enter: ", dropNode.data.apiGroupName);
    },
    handleDragLeave(draggingNode, dropNode, ev) {
      console.log("tree drag leave: ", dropNode.data.apiGroupName);
    },
    handleDragOver(draggingNode, dropNode, ev) {
      console.log("tree drag over: ", dropNode.data.apiGroupName);
    },
    handleDragEnd(draggingNode, dropNode, dropType, ev) {
      console.log(
        "tree drag end: ",
        dropNode && dropNode.data.apiGroupName,
        dropType
      );
      // 调后端更新
      this.updateApiGroup(this.data);
    },
    handleDrop(draggingNode, dropNode, dropType, ev) {
      console.log("tree drop: ", dropNode.data.apiGroupName, dropType);
    },
    allowDrop(draggingNode, dropNode, type) {
      if (dropNode.data.id === 1) {
        return false;
      } else {
        return true;
      }
    },
    allowDrag(draggingNode) {
      // 顶层默认分组不允许拖拽
      if (draggingNode.data.id === 1) {
        return false;
      } else {
        return true;
      }
      // return draggingNode.data.apiGroupName.indexOf('三级 3-2-2') === -1
    },

    append(node, data) {
      // var pid = data.parentApiGroupId + ':' + data.id
      var uuid = this.common.getUuid();
      const newChild = {
        id: uuid,
        isEdit: 0,
        apiGroupName: "T" + uuid,
        children: [],
      };
      if (!data.children) {
        this.$set(data, "children", []);
      }
      data.children.push(newChild);
      this.updateApiGroup(this.data);
    },

    remove(node, data) {
      const parent = node.parent;
      const children = parent.data.children || parent.data;
      const index = children.findIndex((d) => d.id === data.id);
      children.splice(index, 1);
      this.updateApiGroup(this.data);
    },

    edit(node, data) {
      console.log(
        "before:",
        data.id,
        // data.parentApiGroupId,
        data.apiGroupName,
        data.isEdit
      );
      this.$set(data, "isEdit", 1);
      this.newApiGroupName = data.apiGroupName;
      this.$nextTick(() => {
        this.$refs.input.focus();
      });
      console.log("after:", data.id, data.apiGroupName, data.isEdit);
    },

    submitEdit(node, data) {
      // console.log('点击了保存按钮')
      if (data.apiGroupName == this.newApiGroupName) {
        console.log("没有修改");
        this.newApiGroupName = "";
        this.$set(data, "isEdit", 0);
      } else {
        this.$set(data, "apiGroupName", this.newApiGroupName);
        this.newApiGroupName = "";
        this.$set(data, "isEdit", 0);
        // console.log('after:', data.id, data.apiGroupName)
        // console.log(this.data)
        this.updateApiGroup(this.data);
      }
    },

    updateApiGroup(data) {
      console.log(data, '数据');
      // updateApiGroup(1, data)
      //   .then(response => {
      //     console.log(response)
      //   })
      //   .catch(err => {
      //     console.log(err)
      //   })
    },

    nodeclick(node, data, obj) {
      console.log("点击了：", node.id, node.apiGroupName);
    }