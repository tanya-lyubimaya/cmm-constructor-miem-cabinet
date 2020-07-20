<template>
  <div class="wraper">
    <div class="navigation">
      <section class="container">
        <a
          class="navigation-title"
          href="/enter"
          title="База КИМов - Сервис для преподавателей МИЭМ НИУ ВШЭ"
        >
          <h1 class="title">База КИМов</h1>
        </a>
      </section>
    </div>
    <el-table v-if="cmms.length > 0" ref="singleTable" :data="cmms" style="margin: 7%" @cell-click="handle">
      <el-table-column
        prop="spreadsheetName"
        label="Имя КИМа"
        width="300"
      />
      <el-table-column
        prop="spreadsheetUrl"
        label="Сслыка на таблицу"
        width="450"
      />
    </el-table>
    <section class="container" v-if="chosen" id="base">
      <h4>Заполните данные для генерации вариантов из КИМа "{{ currentCmm }}" </h4>
      <div v-if="spreadsheetInfo">
        <el-form>
          <p>Укажите количество вопросов из каждого раздела</p>
          <el-form v-for="info in spreadsheetInfo" :key="info.title">
            <label for="info.title"><p>{{ info.title }}</p></label>
            <el-select ref="selectTopics" name="info.title" v-model="info.value" id="info.title">
              <el-option :key="0" :value="''"></el-option>
              <el-option v-for="i in info.amount" :value="i" :key="i">
                {{ i }}
              </el-option>
            </el-select>
          </el-form>
          <el-form style="margin-top: 1rem">
            <label for="amountOfVarients"><p>Укажите количество вариантов</p></label>
            <el-input
              v-model="amountOfVariants"
              type="number"
              placeholder="For example, 10"
              name="amountOfVariants"
              id="amountOfVariants"
              min="1">
            </el-input>
          </el-form>
          <el-form-item>
            <div style="margin-top: 1rem">
              <el-button
                type="primary"
                id="submit"
                native-type="submit"
                class="buttonCreate"
                @click="createVariants">Добавить</el-button>
              <el-button
                @click="onCancel"
                class="buttonCancel">Отменить</el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      cmms: [],
      currentCmm: '',
      chosen: false,
      amountOfVariants: '',
      spreadsheetName: 'test #1',
      spreadsheetId: '333',
      spreadsheetInfo: [
        { title: 'Geography', amount: 5, value: '' },
        { title: 'Biology', amount: 10, value: '' },
        { title: 'Maths', amount: 7, value: '' }]
    }
  },
  created() {
    this.getCmms();
  },
  methods: {
    onSubmit() {
      // this.$message('submit!')
      // const spreadsheetInfo = JSON.parse(this.dataset.spreadsheetInfo);
      // const spreadsheetId = this.dataset.spreadsheetId;
      // createVariants(spreadsheetInfo,spreadsheetId);
    },
    createVariants(spreadsheetInfo,spreadsheetId) {
      let amount = this.amountOfVariants;
      let questions = [];
      let inpInfo = this.$refs.selectTopics;

      for (let i = 0; i < inpInfo.length; i++) {
        questions.push(inpInfo[i].value);
      }
      const questionsAsString = questions.join(',');
      // window.location.href = `/create_variants?questions=${questionsAsString}&amount=${amount}&spreadsheet_id=${spreadsheetId}`;
    },
    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    },
    getCmms() {
      console.log('started method getCmms()')
      const path = 'http://localhost:5000/get_cmms'
      axios.get(path).then(
        res => {
          this.cmms = res.data
        },
        error => {
          console.error(error)
        },
      )
    },
    handle(row) {
      this.chosen = true;
      this.currentCmm = this.cmms[this.cmms.indexOf(row)].spreadsheetName
      // сделать обработку
    }
    /*function createVariants(spreadsheetInfo, spreadsheetId) {
        let amount = $('#amountOfVariants').val();
        let questions = [];
        document
            .querySelectorAll('.select-topics')
            .forEach(select => questions.push($(select).val()));
        const questionsAsString = questions.join(',');
        window.location.href = `/create_variants?questions=${questionsAsString}&amount=${amount}&spreadsheet_id=${spreadsheetId}`;
    }*/
  }
}
</script>
