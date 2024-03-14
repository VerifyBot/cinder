<template>
  <v-main class="bg-surface py-5 swipe-cont">
    <v-container v-if="loading">
      <v-row class="fill-height" align="center" justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-progress-linear indeterminate color="red-darken-2"></v-progress-linear>
        </v-col>
      </v-row>
    </v-container>


    <v-container class="mx-0" v-if="!serverDown && !loading">
      <v-row class="mx-auto">
        <span class="swipe-hello" v-if="!isMobile && !serverDown">
          Logged in as {{ username }}
        </span>
      </v-row>

      <v-row :style="'min-width: 99vw;' + (isMobile ? 'flex-direction: column-reverse;' : '')" class="px-0">
        <v-col md="2">
          <v-sheet rounded="lg" style="height: 70vh" class="bg-primary">
            <div class="text-h5 text-center py-2">Conversations
              <span v-if="chats.length > 0"><v-chip prepend-icon="mdi-delete" size="small" class="hover-chip"
                  color="red-lighten-2" @click="clearChats">Clear</v-chip></span>

            </div>
            <v-virtual-scroll height="55vh" :items="chats">
              <template v-slot:default="{ item }">
                <v-list-item class="chat" @click="onChatClick(item)">
                  <template v-slot:prepend>
                    <v-avatar color="grey-darken-1">

                      <v-img cover :src="item.car_img" style="transform: scale(1.56)"></v-img>
                    </v-avatar>
                  </template>
                  <div style="color: #aaa">
                    <v-icon>mdi-car-hatchback</v-icon>
                    Car Manager
                  </div>

                  <v-list-item-title :title="item.car_name" class="car-list-item-title">{{ item.car_name
                    }}</v-list-item-title>

                </v-list-item>

                <v-divider inset></v-divider>
              </template>
            </v-virtual-scroll>
            <!-- <v-list lines="two">
                <template v-for="n in 15" :key="n">
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-avatar color="grey-darken-1"></v-avatar>
                    </template>

                    <v-list-item-title :title="`Message ${n}`"></v-list-item-title>

                    <v-list-item-subtitle title="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Nihil repellendus distinctio similique"></v-list-item-subtitle>
                  </v-list-item>

                  <v-divider
                    v-if="n !== 6"
                    :key="`divider-${n}`"
                    inset
                  ></v-divider>
                </template>
              </v-list> -->
          </v-sheet>
        </v-col>
        <v-divider v-if="isMobile"></v-divider>
        <v-col md="7">
          <v-sheet id="car-frame" rounded="lg" class="bg-primary"
            style="height: min-content; position: relative !important;" @pointerdown="onPointerDown"
            @pointermove="onPointerMove" @pointerup="onPointerUp" @pointerleave="onPointerUp">

            <div v-if="imageViewModel === 0">
              <v-img :src="'data:image/png;base64,' + carImage" class="secondary" aspect-ratio="16/9">

                <template v-slot:placeholder>
                  <v-row class="fill-height ma-0" align="center" justify="center">
                    <!-- <v-img src="https://www.montway.com/app/uploads/2022/01/montway_39-1.jpg" aspect-ratio="16/9"></v-img> -->
                    <v-progress-circular indeterminate color="amber"></v-progress-circular>
                  </v-row>
                </template>
              </v-img>
            </div>

            <div v-else>
              <v-row>
                <v-col v-for="n in Math.max(Math.min(carDataItems.extraImages.length, 9), 7)" :key="n"
                  class="d-flex child-flex" cols="4" style="height: calc(70vh/3) !important;">
                  <v-img v-if="n < carDataItems.extraImages.length" :src="carDataItems.extraImages[n - 1]"
                    aspect-ratio="16/9" class="bg-grey-lighten-2 image">

                    <template v-slot:placeholder>
                      <v-row class="fill-height ma-0" align="center" justify="center">
                        <v-progress-circular indeterminate color="grey-lighten-5"></v-progress-circular>
                      </v-row>
                    </template>
                  </v-img>
                </v-col>
              </v-row>
            </div>

            <v-btn @click="carLike" color="#00C853" icon="mdi-heart-multiple"
              style="position: absolute; top: 50%; transform: translate(30%, -50%); left: 0; color: white"></v-btn>
            <v-btn @click="carDislike" color="#ff6a6c" icon="mdi-thumb-down"
              style="position: absolute; top: 50%; transform: translate(-30%, -50%); right: 0"></v-btn>

            <!-- 
              https://vuetifyjs.com/en/directives/touch/#usage
             -->
          </v-sheet>

          <v-sheet rounded="lg" class="bg-primary d-flex align-center justify-center pb-3"
            style="width: 100%; text-align: center;">

            <div class="d-flex flex-column">
              <v-slide-group v-model="imageViewModel">
                <v-slide-group-item key="main" v-slot="{ isSelected, toggle }">
                  <v-btn class="ma-2" rounded :color="isSelected ? 'info' : undefined" @click="toggle">
                    Main Image
                  </v-btn>
                </v-slide-group-item>
                <v-slide-group-item key="extra" v-slot="{ isSelected, toggle }">
                  <v-btn class="ma-2" rounded :color="isSelected ? 'info' : undefined" @click="toggle">
                    Extra Images
                  </v-btn>
                </v-slide-group-item>
              </v-slide-group>

              <v-footer class="d-flex my-2">
                <v-chip prepend-icon="mdi-menu-swap-outline" :color="methodColor" size="large" class="hover-chip"
                  @click="changeRecommendation">
                  Recommendation method (<strong>{{ methodTitle }}</strong>)
                </v-chip>
                <v-chip color="red-darken-1" prepend-icon="mdi-close-octagon" size="large" class="ml-3 hover-chip"
                  @click="resetRecommendation">
                  Reset recommendation
                </v-chip>
              </v-footer>

              <!-- <span v-if="carDataItems && carDataItems.similarity">I am {{ Math.round(carDataItems.similarity * 100) }}%
                certain that you are going to like that</span> -->
            </div>


          </v-sheet>

        </v-col>
        <v-divider v-if="isMobile"></v-divider>
        <v-col md="3" class="car-info-items">
          <v-sheet rounded="lg" min-height="35vh" class="bg-primary info-block">
            <div class="text-h5 text-center pt-2">Car Info </div>
            <div class="text-h6 text-center" id="car-name" style="direction: rtl;">
              {{ carDataItems.company }} {{ carDataItems.name }}</div>
            <v-container id="car-attrs">
              <v-row no-gutters>
                <v-col>

                  <v-sheet class="pa-2 ma-2 info-block">
                    <div>
                      <v-icon color="orange">mdi-cash</v-icon>
                      <span class="ml-2" v-if="!isMobile">price: </span>
                      <code>{{ formatCurrency(carDataItems.price) }}</code>
                    </div>
                  </v-sheet>
                </v-col>

                <v-col>
                  <v-sheet class="pa-2 ma-2 info-block">
                    <div>
                      <v-icon :style="'color: ' + pollutionColor(carDataItems.pollution)">mdi-air-filter</v-icon>
                      <span class="ml-2">pollution: </span>
                      <code :style="'color: ' + pollutionColor(carDataItems.pollution)">
                {{ carDataItems.pollution }}/15
              </code>
                    </div>

                  </v-sheet>
                </v-col>
                <!-- 
                <v-col>
                  <v-sheet class="pa-2 ma-2 info-block">
                    <div>
                      <v-icon color="light-green">mdi-palette</v-icon>
                      <span class="ml-2" v-if="!isMobile">color: </span>
                      <code :style="'color: ' + carDataItems.color + '; border: 1px solid white; font-weight: bold;'">
                                                            {{ carDataItems.color }}
                                                            </code>
                    </div>
                  </v-sheet>
                </v-col> -->

                <v-responsive width="100%"></v-responsive>

                <v-col>
                  <v-sheet class="pa-2 ma-2 info-block">
                    <div>
                      <v-icon color="purple-lighten-2">mdi-weight</v-icon>
                      <span class="ml-2" v-if="!isMobile">weight: </span>
                      <code>
                {{ carDataItems.weight }}kg
              </code>
                    </div>
                  </v-sheet>
                </v-col>

                <v-col>
                  <v-sheet class="pa-2 ma-2 info-block">
                    <div>
                      <v-icon color="deep-purple">mdi-engine</v-icon>
                      <span class="ml-2">engine: </span>
                      <code v-if="carDataItems.engineType">{{ engineTypes[carDataItems.engineType] }}</code>
                      <code v-else>N/A</code>
                    </div>
                  </v-sheet>
                </v-col>


                <v-responsive width="100%"></v-responsive>

                <v-col>
                  <v-sheet class="pa-2 ma-2 info-block">
                    <div>
                      <v-icon color="pink-lighten-2">mdi-speedometer</v-icon>
                      <span class="ml-2">0-100 time: </span>
                      <code>
                {{ carDataItems.maxAcceleration }}s
              </code>
                    </div>
                  </v-sheet>
                </v-col>


                <v-col>
                  <v-sheet class="pa-2 ma-2 info-block">
                    <div>
                      <v-icon color="brown-lighten-2">mdi-resize</v-icon>
                      <span class="ml-2">H x W x L: </span>
                      <code>
                {{ carSize(carDataItems.height) }}m x {{ carSize(carDataItems.width) }}m x {{
      carSize(carDataItems.length) }}m
              </code>
                    </div>
                  </v-sheet>
                </v-col>

                <v-responsive width="100%" class="mt-2"></v-responsive>

                <v-col>
                  <v-sheet class="pa-2 ma-2 info-block">
                    <div>
                      <v-icon color="amber">mdi-gas-station</v-icon>
                      <span class="ml-2">fuel tank: </span>
                      <code v-if="carDataItems.fueltankCapacity">{{ carDataItems.fueltankCapacity }}L</code>
                      <code v-else>N/A</code>
                    </div>
                  </v-sheet>
                </v-col>

                <v-col>
                  <v-sheet class="pa-2 ma-2 info-block">
                    <div>
                      <v-icon color="indigo-lighten-3">mdi-barrel</v-icon>
                      <span class="ml-2">est. range: </span>
                      <code v-if="carDataItems.fuelConsumptionUrban && carDataItems.fueltankCapacity">{{
      (carDataItems.fueltankCapacity / carDataItems.fuelConsumptionUrban).toFixed(0) * 100 }}km</code>
                      <code v-else>N/A</code>
                    </div>
                  </v-sheet>
                </v-col>

                <v-responsive width="100%" class="mt-2"></v-responsive>



                <v-col>
                  <v-sheet class="pa-2 ma-2 info-block">
                    <div>
                      <v-icon color="cyan-darken-1">mdi-cog</v-icon>
                      <span class="ml-2">gearbox: </span>
                      <code>
                {{ {
      "ידנית": "manual", "אוטומטית": "automatic", "רובוטית": "robotic", "רציפה": "CVT", "תמסורת ישירה":
        "direct"
    }[carDataItems.gearbox] }}
              </code>
                    </div>
                  </v-sheet>
                </v-col>

                <v-col>
                  <v-sheet class="pa-2 ma-2 info-block">
                    <div>
                      <v-icon color="blue-grey-lighten-1">mdi-tire</v-icon>
                      <span class="ml-2">drivetrain: </span>
                      <code>{{ vehiclePropulsions[carDataItems.vehiclePropulsion] }}</code>
                    </div>
                  </v-sheet>
                </v-col>


                <!-- <v-responsive width="100%" class="mt-2"></v-responsive> -->

                <v-responsive width="100%" class="mt-2"></v-responsive>


                <div class="features d-flex justify-center flex-wrap" style="width: 100%;">
                  <v-chip v-if="carDataItems.cruiseControl" color="blue-lighten-3"
                    prepend-icon="mdi-car-cruise-control">בקרת
                    שיוט</v-chip>
                  <v-chip v-if="carDataItems.smartscreen" color="orange-lighten-3" prepend-icon="mdi-multimedia">מערכת
                    מולטימדיה</v-chip>
                  <v-chip v-if="carDataItems.sunroof" color="yellow-lighten-3"
                    prepend-icon="mdi-white-balance-sunny">חלון
                    בגג</v-chip>
                </div>
              </v-row>
            </v-container>
          </v-sheet>
        </v-col>
      </v-row>

      <v-dialog v-model="chatDialog" width="800px">
        <v-card>
          <v-card-actions>
            <v-btn block @click="chatDialog = false" color="error">Leave chat</v-btn>
          </v-card-actions>
          <v-card-text style="height: 70vh;" class="pt-0 pb-1">
            <v-divider class="mb-5"></v-divider>

            <!-- <div class="messages">
              <div class="bg-red pa-2" style="border-radius: 10px">
                Hi there!
              </div>

              <div class="bg-blue pa-2" style="border-radius: 10px">
                Heyooo
              </div>
            </div>
            <v-textarea id="chat-input" rows="2" row-height="20" clearable auto-grow label="Label" variant="outlined"></v-textarea> -->
            <section class="msger">
              <header class="msger-header">
                <v-avatar color="grey-darken-1">
                  <v-img cover :src="chatCar?.image" style="transform: scale(1.56)">
                  </v-img>
                </v-avatar>
                <div class="msger-header-title">
                  Car Manager ({{ chatDialogWith?.car_name }})
                </div>
                <div class="msger-header-options">
                  <span>
                    <v-btn color="pink-lighten-2" icon="mdi-arrow-down-right-bold" variant="tonal"
                      @click="chatScrollBottom"></v-btn>
                  </span>
                </div>
              </header>
              <v-virtual-scroll class="msger-chat" :items="chatMessages" ref="chatVScroller">

                <template v-slot:default="{ item }">
                  <div class="mb-2"></div>
                  <div :class="'msg ' + (item.is_bot ? 'left-msg' : 'right-msg')">
                    <div class="msg-bubble">
                      <div class="msg-info">
                        <div class="msg-info-name">{{ item.is_bot ? 'BOT' : 'YOU' }}</div>
                        <div class="msg-info-time">
                          {{
      new Date(item.created_at).toLocaleTimeString('he-IL', { hour: '2-digit', minute: '2-digit' })
    }}
                        </div>
                      </div>

                      <div class="car-img-chat msg-text" v-if="item.content === 'IMG@'">
                        <v-img :src="chatCar.image" aspect-ratio="16/9" style="border-radius: 10px">
                        </v-img>


                      </div>

                      <div class="msg-text" v-else>
                        {{ item.content }}
                      </div>
                    </div>
                  </div>

                </template>
              </v-virtual-scroll>

              <v-form v-model="sendForm" @submit.prevent="sendMessage">
                <v-text-field auto-grow row-height="15" style="max-height: 10%" label="Write your message"
                  variant="underlined" rows="1" v-model="sendContent" class="mt-2">
                  <!-- append-icon slot of mdi-send -->

                  <template v-slot:append>
                    <v-btn color="green-darken-2" fab small type="submit" :disabled="!sendForm"
                      :loading="waitingMessage">
                      <v-icon>mdi-send</v-icon>
                    </v-btn>
                  </template>

                </v-text-field>
              </v-form>

            </section>


          </v-card-text>

        </v-card>
      </v-dialog>

    </v-container>

    <v-container v-if="serverDown && !loading">
      <v-row class="fill-height" align="center" justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-alert dense outlined type="error" color="red-darken-2" elevation="2" border="left" icon="mdi-server-off">
            Server is not available.
          </v-alert>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>


<script>
import $ from "@/jquery.min.js";
import notify from "@/notify.min.js"

export default {
  data: () => ({
    username: 'loading...',
    serverDown: false,
    loading: true,

    isMobile: false,
    chatDialog: false,

    carDataItems: {},
    carImage: null,

    imageViewModel: 0,  // 0 - main , 1 - extra

    chatVScroller: null,

    chats: [],

    chatDialogWith: null,
    chatMessages: [],
    sendContent: "Let's negotiate the price.",
    waitingMessage: false,
    sendForm: false,
    chatCar: null,

    startX: 0,
    startY: 0,
    moveX: 0,
    moveY: 0,
    current: null,
    dragEventsRelevant: false,

    methodName: "loading...",
    methodTitle: "loading...",
    methodColor: null,

    engineTypes: {
      "בנזין": "gasoline", "דיזל": "diesel", "הייבריד בנזין":
        "hybrid", "הייבריד דיזל": "hybrid"
    },

    vehiclePropulsions: {
      "קדמית": "FWD", "אחורית": "RWD", "כפולה קבועה": "4X4", "אחורית + כפולה": "RWD & 4X4",
      "קדמית + כפולה": "FWD & 4X4"
    },

    methodColors: {
      "average": "blue-lighten-2",
      "weighted": "orange-lighten-2",
    }
  }
  ),
  async mounted() {
    let resp = await this.api.get('/me');

    if (resp.error && resp.error === "Connection Error") {
      this.loading = false;
      this.serverDown = true;

      return
    }

    this.username = localStorage.getItem('username');

    this.isMobile = window.innerWidth < 1283;

    // on screen size change
    window.addEventListener('resize', () => {
      this.isMobile = window.innerWidth < 1283;
    })

    // get car and chats
    this.loadNextCar();
    this.loadChats();

    // get recommendation method
    this.api.get('/method').then(async js => {
      this.methodName = js.data.method;
      this.methodTitle = js.data.method.charAt(0).toUpperCase() + js.data.method.slice(1);
      this.methodColor = this.methodColors[js.data.method]

    })


    this.loading = false;

    // swipe
    await this.$nextTick();  // wait for element to be rendered     
    this.current = document.getElementById('car-frame')

  },


  methods: {
    async changeRecommendation() {
      const js = await this.api.post('/methodChange');
      this.methodName = js.data.method;
      this.methodTitle = js.data.method.charAt(0).toUpperCase() + js.data.method.slice(1);
      this.methodColor = this.methodColors[js.data.method]
    },

    async resetRecommendation() {
      await this.api.post('/recommendationReset');
      this.loadNextCar();
    },

    async clearChats() {
      const js = await this.api.post('/clearChats');
      this.chats = [];
    },

    async sendMessage() {
      if (!this.sendForm || !this.sendContent) return;

      this.waitingMessage = true;

      this.chatMessages.push({
        content: this.sendContent,
        created_at: new Date().toISOString(),
        is_bot: false
      });

      await this.$nextTick();

      // scroll to bottom
      this.chatScrollBottom();

      let sendTemp = this.sendContent
      this.sendContent = '';


      // send message to server
      const js = await this.api.post('/send', {
        car_id: this.chatDialogWith.car_id,
        content: sendTemp
      });



      if (js.error) {
        notify(`⚠️ ${js.error}`, {
          position: "bottom left",
          className: "error",
          autoHideDelay: 3000,
        });
      } else {
        this.chatMessages.push({
          content: js.data.message.content,
          created_at: js.data.message.created_at,
          is_bot: true
        });

        // scroll to bottom
        this.chatScrollBottom();
      }

      this.waitingMessage = false;
    },

    async chatScrollBottom() {
      this.$refs.chatVScroller.scrollToIndex(this.chatMessages.length - 1);
      await this.$nextTick();
      setTimeout(() => {
        this.$refs.chatVScroller.scrollToIndex(this.chatMessages.length - 1);
      }, 10);
    },

    async onChatClick(chat) {
      this.chatMessages = [];
      this.chatDialog = true;
      const js = await this.api.get(`/chat?car_id=${chat.car_id}`);
      this.chatMessages = js.data.messages;
      this.chatDialogWith = chat;
      this.chatCar = js.data.car;
      // this.chatScrollBottom();
    },
    ///
    setTransform(x, y, deg, duration) {
      this.current.style.transform = `translate3d(${x}px, ${y}px, 0) rotate(${deg}deg)`
      if (duration) this.current.style.transition = `transform ${duration}ms`
    },

    onPointerDown(ev) {
      ev.preventDefault();
      const { clientX, clientY } = ev;
      this.startX = clientX;
      this.startY = clientY;

      this.dragEventsRelevant = true;
    },

    onPointerMove({ clientX, clientY }) {
      if (!this.dragEventsRelevant) return;

      this.moveX = clientX - this.startX;
      this.moveY = clientY - this.startY;
      this.setTransform(this.moveX, this.moveY, this.moveX / window.innerWidth * 50)
    },

    onPointerUp() {
      if (!this.dragEventsRelevant) return;
      this.dragEventsRelevant = false;
      // console.log(`POP moveX: ${this.moveX}`)

      if (Math.abs(this.moveX) > this.current.clientWidth / 2) {
        // console.log("calling complete")
        this.current.removeEventListener('pointerdown', this.onPointerDown)
        this.complete()
      } else this.cancel()

      this.moveX = 0;
      this.moveY = 0;

    },

    complete() {
      const flyX = (Math.abs(this.moveX) / this.moveX) * window.innerWidth * 1.3
      const flyY = (this.moveY / this.moveX) * flyX
      this.setTransform(flyX, flyY, flyX / window.innerWidth * 50, window.innerWidth);

      this.dragEventsRelevant = false;
      setTimeout(async () => {
        await this.carLike();
        this.current.style.transition = ''
        this.current.style.transform = ''
        this.setTransform(0, 0, 0, 0)
      }, 300)
    },

    cancel() {
      this.setTransform(0, 0, 0, 100);
      setTimeout(() => {
        this.current.style.transition = ''
        this.current.style.transition = ''
      }, 100);
      this.dragEventsRelevant = false;
    },

    ///



    async carLike() {
      this.carImage = null;
      this.imageViewModel = 0;

      // user likes current car
      const js = await this.api.post("/swipe", { car_id: Number(this.carDataItems.id), like: true });
      this.showNewChatIfAny(js);
      await this.loadNextCar();

    },

    async carDislike() {
      this.carImage = null;
      this.imageViewModel = 0;

      // user dislikes current car
      const js = await this.api.post("/swipe", { car_id: Number(this.carDataItems.id), like: false });
      this.showNewChatIfAny(js);
      await this.loadNextCar();

    },

    showNewChatIfAny(js) {
      console.table(js.data)
      if (js?.data.new_chat) {
        this.chats.push(js.data.chat);
        notify(`🎉 New chat with ${js.data.chat.car_name}!`, {
          position: "bottom left",
          className: "success",
          autoHideDelay: 3000,
        });
      }
    },

    async loadNextCar() {
      const resp = await this.api.get("/car");

      if (!resp?.ok) {
        // show alert
        notify(`⚠️ ${resp?.error || 'API is not available.'}`, {
          position: "bottom left",
          className: "error",
          autoHideDelay: 3000,
        });
        return;
      }

      const js = resp.data;

      // car image is in js.image, it is base64
      this.carImage = js.image;
      delete js.image;
      this.carDataItems = js;

      // change to main image view
      this.imageViewModel = 0;

    },

    async loadChats() {
      const resp = await this.api.get('/chats');
      this.chats = resp.data.chats;
    },

    carSize(v) {
      return (v / 1000).toFixed(2);
    },
    formatCurrency(v) {
      const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'ILS',
        maximumFractionDigits: 0,
      });

      return formatter.format(v);
    },

    pollutionColor(v) {
      return '#' + [
        // 15 different pollution colors (from good to bad)
        '84FFFF', '039BE5', '007d44', '009442', '00a73c', '00bc33',
        '9ad100', 'fff400', 'ffcb00', 'ffa300', 'ff7a00', 'ff4c00',
        'eb2400', 'db0020', 'b51a2b'
      ][v - 1]
    }

  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Pixelify+Sans&family=Suez+One&display=swap');

.hover-chip {
  cursor: pointer;
}

.hover-chip:hover {
  filter: brightness(1.2);
}

.car-list-item-title {
  direction: rtl;
}

.swipe-hello {
  font-size: 1.5rem;
  font-weight: bold;

  /* gradient */
  /* gradient color, blue-pink */
  background: linear-gradient(45deg, #a29ff9 0%, #d6a7ff 80%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.swipe-cont[class^="text"] {
  text-decoration: underline;
}

.swipe-cont span,
.swipe-cont div,
.swipe-cont code,
[class^="text"] {
  font-family: 'Gabarito', sans-serif !important;
}

#car-attrs span {
  font-family: 'Pixelify Sans', sans-serif !important;
}


#car-name {
  font-family: "Suez One", serif !important;
  font-size: 1.5rem !important;
  background: -webkit-linear-gradient(#f91858, #f6c967);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>

<style>
.chat:hover {
  cursor: pointer;
  background-color: #1f222e;
  border-radius: 5px;
}

.messages {
  display: flex;
  flex-direction: column;
  /* space between flex items */
}

.messages>* {
  margin-bottom: 20px;

  /* textbox in the bottom of messages*/
}

:root {
  --body-bg: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  --msger-bg: #fff;
  --border: 2px solid #ddd;
  --left-msg-bg: #ececec;
  --right-msg-bg: #579ffb;
}


.msger {
  display: flex;
  flex-flow: column wrap;
  justify-content: space-between;
  /* width: 100%; */
  /* max-width: 867px; */
  /* margin: 25px 10px; */
  height: calc(100% - 50px);
  /* box-shadow: 0 15px 15px -5px rgba(0, 0, 0, 0.2); */
}



.msger-chat {
  width: 100%;
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.msger-chat::-webkit-scrollbar {
  width: 6px;
}

.msger-chat::-webkit-scrollbar-track {}

.msger-chat::-webkit-scrollbar-thumb {}

.msg {
  display: flex;
  align-items: flex-end;
  margin-bottom: 10px;
}

.msg:last-of-type {
  margin: 0;
}

.msg-img {
  width: 50px;
  height: 50px;
  margin-right: 10px;
  background: #ddd;
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
  border-radius: 50%;
}

.msg-bubble {
  max-width: 85%;
  padding: 15px;
  border-radius: 15px;
  background: #2c3247;
}

.msg-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.msg-info-name {
  margin-right: 10px;
  font-weight: bold;
}

.msg-info-time {
  font-size: 0.85em;
}

.left-msg .msg-bubble {
  border-bottom-left-radius: 0;
}

.right-msg {
  flex-direction: row-reverse;
}

.right-msg .msg-bubble {
  background: #0097e6;
  color: #fff;
  border-bottom-right-radius: 0;
}

.right-msg .msg-img {
  margin: 0 0 0 10px;
}

.msger-inputarea {}

.msger-header {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: var(--border);
  border: 2px solid #3a4047;
  border-radius: 20px;
  color: #fff;
  font-weight: bold;
}

.msger-header-title span {
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
}

.swipe-cont code {
  background-color: darkslategrey;
  margin-left: 5px;
}

.features>* {
  margin: .25rem !important;
  font-weight: bold;
}

.car-info-items .info-block {
  border-radius: 5px;
}

.image img {
  object-fit: none !important;
}

#car-frame,
#car-frame * {
  user-select: none !important;
  touch-action: none !important;
}

.v-sheet.info-block {
  border: 1px solid #3a4047;
}

.car-img-chat:hover {
  transform: scale(6) !important;
  padding-left: 2rem;
}
</style>