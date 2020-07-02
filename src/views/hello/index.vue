<template>
  <div class="app-container">
    <el-alert
      v-loading="textLoading"
      element-loading-text="Loading hello world"
      :closable="false"
      :title="text"
    >
        <template slot-scope="scope">
          {{ scope.text }}
        </template>
    </el-alert>
  </div>
</template>

<script>
import { getList } from '@/api/hello'

export default {
  data() {
    return {
      text: null,
      textLoading: true
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.textLoading = true
      getList().then(response => {
        this.text = response.data.items
        this.textLoading = false
      })
    }
  }
}
</script>