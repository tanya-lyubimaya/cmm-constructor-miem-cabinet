<template>
    <div class="wrapper">
        <div class="navigation">
            <section class="container">
                <a class="navigation-title" href="/enter" title="База КИМов - Сервис для преподавателей МИЭМ НИУ ВШЭ">
                    <h1 class="title">База КИМов</h1>
                </a>
            </section>
        </div>
        <section class="container" id="variants-data">
            <h4>Заполните данные для раздачи вариантов из КИМа "{{ spreadsheetName }}"</h4>
            <div v-if="courses">
                <el-form>
                    <label for="course"><p>Выберите курс</p></label>
                    <el-select 
                        name="course"
                        required
                        id="course"
                        v-model="selectedCourse">
                        <el-option :key="0" :value="''"></el-option>
                        <el-option v-for="i in courses" :value="i.courseName" :key="i.courseName">
                        {{ i.courseName }}
                        </el-option>
                    </el-select>

                    <label for="taskName"><p>Укажите название задания</p></label>
                    <el-input 
                        v-model="taskName" 
                        required
                        name="taskName" 
                        placeholder="For example, Task #1"></el-input>
                    
                    <el-form-item>
                      <p>Выберите время публикации</p>
                      <p>Начало</p>
                      <el-col :span="4">
                        <el-date-picker required v-model="startDate" type="date" placeholder="Pick a date" style="width: 100%;" />
                      </el-col>
                      <el-col :span="5">
                        <el-time-picker required v-model="startTime" type="fixed-time" placeholder="Pick a time" style="width: 100%;" />
                      </el-col>
                    </el-form-item>
                    <el-form-item>
                      <p>Окончание</p>
                      <el-col :span="4">
                        <el-date-picker required v-model="endDate" type="date" placeholder="Pick a date" style="width: 100%;" />
                      </el-col>
                      <el-col :span="5">
                        <el-time-picker required v-model="endTime" type="fixed-time" placeholder="Pick a time" style="width: 100%;" />
                      </el-col>
                    </el-form-item>
                    <el-form-item>
                      <div style="margin-top: 1rem">
                        <el-button
                          type="primary" 
                          id="submit" 
                          native-type="submit" 
                          class="buttonCreate"
                          @click="onSubmit">Сформировать</el-button>
                        <!--el-button 
                          @click="giveOutVariants" 
                          folder_id = {{ folderId }}
                          class="buttonCancel">Отменить</el-button-->
                          <el-button 
                          @click="giveOutVariants" 
                          class="buttonCancel">Отменить</el-button>
                      </div>
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
      courses: [
        {courseName: 'Geography course'},
        {courseName: 'Biology course'},
        {courseName: 'Maths course'}
        ],
        selectedCourse: '',
        taskName: '',
        startDate: '',
        startTime: '',
        endDate: '',
        endTime: '',
        folderId: ''
    }
  },
  methods: {
    giveOutVariants(folder_id) {
      let course = this.selectedCourse;
      let taskName = this.taskName;
      let startDate = this.startDate;
      let startTime = this.startTime;
      let endDate = this.endDate;
      let endTime = this.endTime;
      //window.location.href = `/give_out_variants?course=${course}&taskName=${taskName}&folder_id=${folderId}&startDate=${startDate}&startTime=${startTime}&endDate=${endDate}&endTime=${endTime}`;
    },
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
}
</script> 
<!--
<script>
    function giveOutVariants(folderId) {
        let course = $('#course').val();
        let taskName = $('#taskName').val();
        let start_date = $('#start_date').val();
        let start_time = $('#start_time').val();
        let end_date = $('#end_date').val();
        let end_time = $('#end_time').val();
        window.location.href = `/give_out_variants?course=${course}&task_name=${taskName}&folder_id=${folderId}&start_date=${start_date}&start_time=${start_time}&end_date=${end_date}&end_time=${end_time}`;
    }
</script>
-->
