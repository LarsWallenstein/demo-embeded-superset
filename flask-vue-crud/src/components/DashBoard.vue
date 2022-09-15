/* eslint-disable */
<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-100">
        <h1>Dashboards</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" @click="getDashboard()">
                  Get Dashboard
        </button>
        <br><br>
      </div>
    </div>
    <div class="dashboard"
         id="superset-container">
    </div>
  </div>
</template>
<script>
import axios from 'axios';
import { embedDashboard } from '@superset-ui/embedded-sdk';
// eslint-disable-next-line
export default {
  name: 'DashBoard',
  methods: {
    async fetchGuestTokenFromBackend(dashboardId) {
      const path = 'http://localhost:5000/guest_token';
      return axios.get(path, { params: { id: dashboardId } })
        .then((res) => res.data.guest_token)
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getDashboard(dashboardId = 'f93f686e-5672-4917-b0ef-675f8ee8f683') {
      return embedDashboard({
        id: dashboardId,
        supersetDomain: 'http://192.168.39.188:30034',
        mountPoint: document.getElementById('superset-container'),
        fetchGuestToken: async (id = dashboardId) => this.fetchGuestTokenFromBackend(id),
        dashboardUiConfig: { hideChartControls: true, hideTitle: true, hideTab: true },
      });
    },
  },
};
</script>
<style>
.dashboard {
  margin-top: 60px;
  background-color: #fff;
  width: 600px;
  height: 600px;
}
</style>
