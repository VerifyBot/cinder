<template>
  <v-app-bar color="primary" elevation="10">
    <template v-slot:prepend v-if="notAtHome" class="pa-0 ma-0">
      <span>
        <!-- on mdi-home go to home, without loading it again -->
        <v-btn icon @click="$router.push('/')">
          <v-icon color="warning" size="x-large">mdi-home-circle</v-icon>
        </v-btn>
      </span>
    </template>

    <v-app-bar-title :class="{ 'ma-n3': notAtHome }">
      <svg style="vertical-align: -10px;" xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink" id="svg486229" viewBox="0 0 1024 768" height="180px" version="1.1">
        <metadata id="metadata486235">
          <rdf:rdf>
            <cc:work rdf:about="">
              <dc:format>image/svg+xml</dc:format>
              <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage"></dc:type>
            </cc:work>
          </rdf:rdf>
        </metadata>
        <defs id="defs486233">
          <!-- Define your gradients here -->
          <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="0%" spreadMethod="pad">
            <stop offset="0%" stop-color="#FF5733" />
            <stop offset="100%" stop-color="#FFBD33" />
          </linearGradient>

          <linearGradient id="gradient3" x1="0%" y1="0%" x2="100%" y2="0%" spreadMethod="pad">
            <stop offset="0%" stop-color="#5733FF" />
            <stop offset="100%" stop-color="#BD33FF" />
          </linearGradient>
        </defs>

        <g id="logo-group">
          <image xlink:href="" id="container" x="272" y="144" width="480" height="480" transform="translate(0 0)"
            style="display: none;"></image>
          <g id="logo-center" transform="translate(22.700000000000045 0)">
            <image xlink:href="" id="icon_container" x="-22" y="17" style="display: none;"></image>
            <g id="slogan"
              style="font-style:normal;font-weight:500;font-size:32px;line-height:1;font-family:Montserrat;font-variant-ligatures:none;text-align:center;text-anchor:middle"
              transform="translate(0 0)"></g>
            <g id="title"
              style="font-style:normal;font-weight:normal;font-size:72px;line-height:1;font-family:Cunia;font-variant-ligatures:none;text-align:center;text-anchor:middle"
              transform="translate(0 0)">
              <path char id="path486238"
                style="font-style:normal;font-weight:normal;font-size:72px;line-height:1;font-family:Cunia;font-variant-ligatures:none;text-align:center;text-anchor:middle"
                d="m 378.27463,-18.72 q -0.072,-1.008 -0.072,-2.52 0,-1.584 0,-3.744 0,-2.304 0,-3.888 0,-1.584 0.072,-2.592 0.144,-4.968 1.87199,-8.64 1.8,-3.672 4.752,-6.048 2.952,-2.376 6.98401,-3.528 4.03199,-1.224 8.71199,-1.224 4.104,0 8.06401,1.008 4.03199,1.008 7.2,3.168 3.16799,2.16 5.11199,5.472 2.016,3.24 2.088,7.776 0,0.648 -0.432,1.08 -0.504,0.432 -1.152,0.432 h -10.15199 q -1.08001,0 -1.584,-0.432 -0.43201,-0.432 -0.72001,-1.44 -0.936,-3.384 -2.952,-4.824 -1.94399,-1.44 -5.472,-1.44 -8.136,0 -8.424,9 -0.072,1.008 -0.072,2.448 0,1.44 0,3.528 0,2.016 0,3.528 0,1.512 0.072,2.52 0.36,9.072 8.424,9.072 3.16801,0 5.4,-1.44 2.088,-1.512 3.024,-4.896 0.36,-1.152 0.79201,-1.44 0.57599,-0.432 1.512,-0.432 h 10.15199 q 0.648,0 1.152,0.432 0.432,0.432 0.432,1.08 -0.072,4.608 -2.088,7.92 -2.01599,3.312 -5.256,5.472 -3.168,2.088 -7.12799,3.096 -3.96001,0.936 -7.99201,0.936 -4.824,0 -8.85599,-1.152 -3.96001,-1.152 -6.91201,-3.528 -2.952,-2.376 -4.68,-6.048 -1.72799,-3.672 -1.87199,-8.712 z"
                stroke-width="0" stroke-linejoin="miter" stroke-miterlimit="2" fill="#d9d9d9" stroke="#d9d9d9"
                transform="translate(0 333.28) translate(54.694759999999974 -0.9040000000000035) scale(2) translate(-378.20263 50.904)">
              </path>
              <path char id="path486240"
                style="font-style:normal;font-weight:normal;font-size:72px;line-height:1;font-family:Cunia;font-variant-ligatures:none;text-align:center;text-anchor:middle"
                d="m 430.41163,-1.8 v -42.12 q 0,-2.736 1.87199,-4.464 1.872,-1.8 4.39201,-1.8 h 5.76 q 0.86399,0 1.29599,0.504 0.50401,0.504 0.50401,1.296 V -1.8 q 0,0.792 -0.50401,1.296 Q 443.29962,0 442.43563,0 h -10.224 q -0.79201,0 -1.29601,-0.504 -0.50399,-0.504 -0.50399,-1.296 z"
                stroke-width="0" stroke-linejoin="miter" stroke-miterlimit="2" fill="#d9d9d9" stroke="#d9d9d9"
                transform="translate(0 333.28) translate(169.11275999999992 0.5360000000000085) scale(2) translate(-430.41163 50.184)">
              </path>
              <path char id="path486242"
                style="font-style:normal;font-weight:normal;font-size:72px;line-height:1;font-family:Cunia;font-variant-ligatures:none;text-align:center;text-anchor:middle"
                d="m 454.10863,-2.016 v -42.12 q 0,-2.52 1.79999,-4.392 1.8,-1.872 4.464,-1.872 h 2.304 q 0.864,0 1.94401,0.36 1.07999,0.288 2.23199,1.872 4.248,6.624 7.632,11.952 2.08801,3.24 3.24,5.184 1.224,1.872 2.232,3.528 1.08001,1.584 1.8,2.736 0.72001,1.152 0.86401,1.368 0.144,0.144 0.36,0.144 0.35999,0 0.35999,-0.36 v -20.52 q 0,-1.44 0.504,-2.592 0.576,-1.152 1.44,-1.944 0.864,-0.792 2.01601,-1.224 1.15199,-0.504 2.30399,-0.504 h 4.68 q 0.792,0 1.224,0.504 0.50401,0.504 0.50401,1.368 v 46.44 q 0,0.792 -0.50401,1.296 -0.432,0.576 -1.224,0.576 h -8.136 q -1.728,0 -2.448,-1.368 -4.32,-6.624 -7.776,-11.88 -2.15999,-3.168 -3.384,-5.04 -1.224,-1.944 -2.304,-3.528 -1.00799,-1.656 -1.728,-2.736 -0.71999,-1.152 -0.86399,-1.368 -0.21601,-0.216 -0.36001,-0.216 -0.432,0 -0.432,0.36 v 23.976 q 0,0.864 -0.50399,1.368 -0.50401,0.432 -1.36801,0.432 h -9.072 q -0.72,0 -1.296,-0.504 -0.50399,-0.576 -0.50399,-1.296 z"
                stroke-width="0" stroke-linejoin="miter" stroke-miterlimit="2" fill="#d9d9d9" stroke="#d9d9d9"
                transform="translate(0 333.28) translate(226.5067599999999 0.10400000000000631) scale(2) translate(-454.10863 50.4)">
              </path>
              <path char id="path486244"
                style="font-style:normal;font-weight:normal;font-size:72px;line-height:1;font-family:Cunia;font-variant-ligatures:none;text-align:center;text-anchor:middle"
                d="m 505.92725,-1.8 v -42.12 q 0,-2.736 1.872,-4.464 1.944,-1.8 4.392,-1.8 h 14.4 q 4.824,0 8.856,1.152 4.104,1.08 7.128,3.528 3.024,2.376 4.752,6.12 1.728,3.672 1.872,8.784 0.072,1.008 0.072,2.448 0,1.368 0,3.096 0,1.656 0,3.024 0,1.368 -0.072,2.376 Q 548.55125,0 526.95125,0 h -19.224 q -0.792,0 -1.296,-0.504 -0.504,-0.504 -0.504,-1.296 z m 20.664,-8.928 q 4.68,0 6.768,-2.232 2.088,-2.304 2.16,-6.84 0.072,-1.008 0.072,-2.304 0.072,-1.368 0.072,-3.024 0,-1.656 -0.072,-2.952 0,-1.368 -0.072,-2.376 -0.216,-9 -9.288,-9 h -10.8 q 1.656,0 2.808,1.224 1.152,1.152 1.152,2.52 v 22.752 q 0,0.936 0.576,1.584 0.648,0.648 1.656,0.648 z"
                stroke-width="0" stroke-linejoin="miter" stroke-miterlimit="2" fill="#d9d9d9" stroke="#d9d9d9"
                transform="translate(0 333.28) translate(340.14399999999995 0.5360000000000085) scale(2) translate(-505.92725 50.184)">
              </path>
              <path char id="path486246"
                style="font-style:normal;font-weight:normal;font-size:72px;line-height:1;font-family:Cunia;font-variant-ligatures:none;text-align:center;text-anchor:middle"
                d="m 557.74925,-1.944 v -42.12 q 0,-2.736 1.872,-4.464 1.872,-1.8 4.392,-1.8 h 29.376 q 0.72,0 1.296,0.576 0.576,0.576 0.576,1.296 v 7.128 q 0,0.792 -0.576,1.224 -0.504,0.504 -1.296,0.504 h -26.64 q 1.728,0 2.808,1.224 1.152,1.224 1.152,2.664 v 3.024 q 0,0.792 0.576,1.512 0.576,0.72 1.656,0.72 h 15.624 q 1.872,0 1.872,1.872 v 6.48 q 0,1.872 -1.872,1.872 h -21.816 q 1.656,0 2.808,1.152 1.152,1.152 1.152,2.592 v 3.384 q 0,0.792 0.576,1.512 0.648,0.72 1.656,0.72 h 21.024 q 0.792,0 1.296,0.576 0.576,0.504 0.576,1.296 v 7.056 q 0,0.792 -0.576,1.296 -0.576,0.504 -1.296,0.504 h -34.416 q -0.792,0 -1.296,-0.504 -0.504,-0.504 -0.504,-1.296 z"
                stroke-width="0" stroke-linejoin="miter" stroke-miterlimit="2" fill="#d9d9d9" stroke="#d9d9d9"
                transform="translate(0 333.28) translate(453.78799999999984 0.24799999999999756) scale(2) translate(-557.74925 50.328)">
              </path>
              <path char id="path486248"
                style="font-style:normal;font-weight:normal;font-size:72px;line-height:1;font-family:Cunia;font-variant-ligatures:none;text-align:center;text-anchor:middle"
                d="m 646.35087,-0.576 q -0.432,0.432 -1.07999,0.432 h -10.08001 q -2.08799,0 -2.952,-1.944 l -7.272,-14.4 q -0.64799,-1.152 -1.944,-1.152 h -9.504 q 1.87201,0 2.88,1.296 1.08001,1.296 1.08001,2.52 v 11.88 q 0,0.864 -0.50401,1.368 -0.504,0.432 -1.368,0.432 h -9.79199 q -0.79201,0 -1.29601,-0.504 -0.504,-0.504 -0.504,-1.296 v -42.12 q 0,-2.664 1.87201,-4.464 1.87199,-1.8 4.39199,-1.8 h 15.264 q 4.03201,0 7.63201,0.936 3.67199,0.864 6.408,2.808 2.736,1.944 4.39199,5.112 1.65601,3.096 1.65601,7.56 0,4.464 -1.87201,7.848 -1.79999,3.384 -5.76,5.544 -0.576,0.432 -0.576,0.936 0,0.504 0.144,0.792 l 9,16.344 q 0.216,0.432 0.216,0.792 0,0.504 -0.432,1.08 z m -14.616,-33.408 q 0,-2.952 -1.72799,-4.464 -1.65601,-1.584 -4.53601,-1.584 h -12.384 q 1.72801,0 2.808,1.296 1.08,1.224 1.08,2.592 v 5.76 q 0,0.936 0.64801,1.584 0.648,0.648 1.58399,0.648 h 6.264 q 2.88,0 4.53601,-1.44 1.72799,-1.44 1.72799,-4.392 z"
                stroke-width="0" stroke-linejoin="miter" stroke-miterlimit="2" fill="#d9d9d9" stroke="#d9d9d9"
                transform="translate(0 333.28) translate(556.3192399999999 0.24799999999999756) scale(2) translate(-604.01487 50.328)">
              </path>
            </g>
            <image car
              xlink:href="data:image/png;base64,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"
              id="icon" x="661" y="303" width="195" height="195"></image>
          </g>
        </g>
      </svg>

    </v-app-bar-title>


    <template v-slot:append>


      <span>

        <code style="vertical-align: -2px;" id="version">{{ version }}</code>

        <!-- mdi github btn onclick go to github.com -->
        <v-btn icon="mdi-github" onclick="window.open('https://github.com/VerifyBot/cinder')"></v-btn>
      </span>
    </template>
  </v-app-bar>
</template>

<script>

async function sleep(ms) {
  return new Promise((resolve, _) => {
    setTimeout(() => {
      resolve();
    }, ms);
  });
}

export default {
  data() {
    return {
      clicks: 0,
      inTrans: false,
      version: '0.69',

      isMobile: false
    }
  },
  mounted() {

    this.isMobile = window.innerWidth < 1283;

    // on screen size change
    window.addEventListener('resize', () => {
      this.isMobile = window.innerWidth < 1283;
    })

    document.querySelector('svg').addEventListener('click', this.cinderClickHandler);
    this.cinderClickHandler();
  },
  computed: {
    notAtHome() {
      return this.$route.name !== 'Home';
    }
  },
  methods: {
    async cinderClickHandler() {

      if (this.inTrans) return;

      this.clicks++;

      var car = document.querySelector('[car]');
      var chars = Array.from(document.querySelectorAll('[char]'));

      var changeCharColor = (e, i) => e.setAttribute('fill', `url(#gradient${i > .5 ? 1 : 3})`);
      var changeCarColor = (i) => car.style.filter = `hue-rotate(${i > .5 ? 0 : 253}deg)`;

      chars.map(e => changeCharColor(e, Math.random()));
      changeCarColor(Math.random());

      if (this.clicks % 10 == 0) {
        this.inTrans = true; // car transition started

        // consistent color
        let i = Math.random();
        chars.map(e => changeCharColor(e, i));
        changeCarColor(i);

        // give the car acceleration to the right (move it using the x attribute)
        var x = parseInt(car.getAttribute('x'));
        var acc = .5, v = 0;

        // introduce kinematic equations
        const locForm = (t) => x + v * t + acc * t * t * 0.5;
        const velForm = (t) => v + acc * t;


        for (let i = 0; i < 33; i++) {
          x = locForm(i / 10);
          v = velForm(i / 10);

          car.setAttribute('x', x);

          await sleep(20);
        }

        await sleep(500);

        // now give the car acceleration to the left
        acc = -.5, v = 0;

        // flip the car
        car.classList.add('flip')

        for (let i = 0; i < 50; i++) {
          x = locForm(i / 10);
          v = velForm(i / 10);

          // since the car is flipped, we need to flip the x attribute as well (css go brr)
          car.setAttribute('x', x * -1);

          await sleep(30);
        }

        // reset the car
        car.setAttribute('x', 661);
        car.classList.remove('flip')
        this.inTrans = false;

      }


    }
  }
}


</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Kode+Mono:wght@400..700&display=swap');

.flip {
  transform: scaleX(-1);
}

.pretty-title {
  font-family: "Kode Mono", monospace !important;
  font-optical-sizing: auto !important;
  font-weight: 700 !important;
  font-size: 5rem !important;
  font-style: normal !important;

  /* gradient color, blue-pink */
  background: linear-gradient(45deg, #00e0bb 0%, #8E2DE2 80%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>