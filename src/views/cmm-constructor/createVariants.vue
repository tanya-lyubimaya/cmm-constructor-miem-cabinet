<template>
  <div class="wraper">
    <div class="navigation">
      <section class="container">
        <a href="/enter" class="navigation-title">
          <h1 class="title">База КИМов</h1>
        </a>
      </section>
    </div>
    <section class="container" id="ss-data">
      <h4>Заполните данные для генерации вариантов из КИМа {{ spreadsheetName }} </h4>
      <div v-if="spreadsheetInfo">
        <el-form>
          <h4>Укажите количество вопросов из каждого раздела</h4>
          <div v-for="info in spreadsheetInfo" :key="info.title">
          <p>{{ info.title }}</p>
          <el-select name="info.title" id="info.title" class="select-topics">
            <el-option v-for="i in info.amount" :value="i" :key="i">{{ i }}</el-option>
          </el-select>
          </div>
          <h4>Укажите количество вариантов</h4>
          <el-input type="number" placeholder="For example, 10" name="amountOfVariants" id="amountOfVariants" min="1"></el-input>
          <el-form-item>
            <el-button type="primary" native-type="submit" @click="onSubmit">Create</el-button>
            <el-button @click="onCancel">Cancel</el-button>
          </el-form-item>
        </el-form>
        
      </div>
        

    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      spreadsheetName: 'test #1',
      spreadsheetInfo: [
        {title: 'Geography', amount: 5},
        {title: 'Biology', amount: 10},
        {title: 'Maths', amount: 7}
        ]
    }
  },
  methods: {
    onSubmit() {
      this.$message('submit!')
    },
    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    }
}
  
  /*data () {
    spreadsheetInfo: 'true';
    title: "Connect"
  },
  methods: {
    onSubmit() {
      const spreadsheetInfo = JSON.parse(this.dataset.spreadsheetInfo);
      const spreadsheetId = this.dataset.spreadsheetId;
      createVariants(spreadsheetInfo, spreadsheetId);
    },

    createVariants(spreadsheetInfo, spreadsheetId) {

    }
  }*/
}

</script>
