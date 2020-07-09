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
          <el-select ref="selectTopics" name="info.title" v-model="info.value" id="info.title">
            <el-option :key="0" :value="''"></el-option>
            <el-option v-for="i in info.amount" :value="i" :key="i">
              {{ i }}
            </el-option>
          </el-select>
          </div>
          
          <h4>Укажите количество вариантов</h4>
          <el-input 
            v-model="amountOfVariants" 
            type="number" 
            placeholder="For example, 10" 
            name="amountOfVariants" 
            id="amountOfVariants" 
            min="1">
          </el-input>
          
          <el-form-item>
            <el-button
              type="primary" 
              id="submit" 
              native-type="submit" 
              @click="createVariants">Create</el-button>
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
      amountOfVariants: null,
      spreadsheetName: 'test #1',
      spreadsheetId: '333',
      spreadsheetInfo: [
        {title: 'Geography', amount: 5, value: null},
        {title: 'Biology', amount: 10, value: null},
        {title: 'Maths', amount: 7, value: null}
        ]
    }
  },
  methods: {
    onSubmit() {
      //this.$message('submit!')
      //const spreadsheetInfo = JSON.parse(this.dataset.spreadsheetInfo);
      //const spreadsheetId = this.dataset.spreadsheetId;
      //createVariants();
    },
    createVariants() {
      let amount = this.amountOfVariants;
      let questions = [];
      let inpInfo = this.$refs.selectTopics;

      for(let i = 0; i < inpInfo.length; i++) {
        questions.push(inpInfo[i].value);
      }
      const questionsAsString = questions.join(',');
      //window.location.href = `/create_variants?questions=${questionsAsString}&amount=${amount}&spreadsheet_id=${spreadsheetId}`;

    },
    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    }
  }
}
</script>