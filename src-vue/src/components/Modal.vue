<template>
  <div class="modal">
    <div class="modal-bg" @keydown.esc="cancelForm" @click="cancelFormBg" ref="modalBg">
      <div class="modal-wrapper">
        <ModalEdit
          v-if="editMode || !formData.pid"
          :formData="formData"
          :categories="categories"
          @cancelForm="cancelForm"
          @cancel="editMode = false"
          @formSubmission="handleSubmit"
        />
        <ModalView v-else :formData="formData" @delete="handleDelete" @edit="editMode = true"/>
      </div>
    </div>
  </div>
</template>

<script>
import ModalEdit from "./ModalEdit";
import ModalView from "./ModalView";

export default {
  components: {
    ModalEdit,
    ModalView
  },
  data() {
    return {
      editMode: false
    };
  },
  props: {
    formData: Object,
    categories: Array
  },
  methods: {
    cancelFormBg: function(e) {
      if (e.target == this.$refs.modalBg) this.cancelForm();
    },
    cancelForm: function() {
      this.$emit("closeModalWithoutSaving");
    },
    handleDelete: function() {
      this.$emit("deleteHandler", this.formData.pid);
    },
    handleSubmit: function(submissionData) {
      if (this.formData.pid) submissionData.id = this.formData.pid;
      this.$emit("formSubmission", submissionData);
    }
  }
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style lang="scss" scoped>
.modal-bg {
  display: flex;
  justify-content: center;
  align-items: center;

  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: 100%;
  background-color: rgba(#fff, 0.75);
  .modal-wrapper {
    max-height: calc(100% - 60px);
    width: 640px;
    background: #fdfdfc;
    position: relative;
    -webkit-box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3),
      0 0 40px rgba(0, 0, 0, 0.1) inset;
    -moz-box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3),
      0 0 40px rgba(0, 0, 0, 0.1) inset;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3), 0 0 40px rgba(0, 0, 0, 0.1) inset;
    text-align: left;
    &::before,
    &::after {
      content: "";
      position: absolute;
      z-index: -1;
      -webkit-box-shadow: 0 0 20px rgba(0, 0, 0, 0.8);
      -moz-box-shadow: 0 0 20px rgba(0, 0, 0, 0.8);
      box-shadow: 0 0 20px rgba(0, 0, 0, 0.8);
      top: 5%;
      bottom: 0;
      left: 10px;
      right: 10px;
      -moz-border-radius: 100px / 10px;
      border-radius: 100px / 10px;
    }
  }
}
</style>
