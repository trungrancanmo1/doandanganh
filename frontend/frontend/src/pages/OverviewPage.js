import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import Sidebar from "../components/Sidebar";
import axios from "axios";
import PlantPicture from "../assets/plantPicture.jpg";
import { jwtDecode } from "jwt-decode";



const ChartComponent = ({ title, data, color }) => (
    <div className="p-4 bg-white shadow rounded-lg">
        <h3 className="font-bold mb-2">{title}</h3>
        <ResponsiveContainer width="100%" height={200}>
            <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke={color} strokeWidth={2} />
            </LineChart>
        </ResponsiveContainer>
    </div>
);

const DashboardOverview = () => {
  const navigate = useNavigate();
  const [humidityIndex, setHumidityIndex] = useState();
  const [tempIndex, setTempIndex] = useState();
  const [lightIndex, setLightIndex] = useState();
  const [humidityData, setHumidityData] = useState([]);
  const [tempData, setTempData] = useState([]);
  const [lightData, setLightData] = useState([]);


  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      navigate("/login");
      return;
    }
  
    try {
      const decoded = jwtDecode(token);
      const now = Date.now() / 1000;
      if (decoded.exp < now) {
        // Token đã hết hạn
        navigate("/login");
      }
    } catch (err) {
      // Token không hợp lệ
      navigate("/login");
    }
  
    const headers = {
      Authorization: `Bearer ${token}`,
    };
    
    const fetchData = async () => {
      try {

        const [humidity, temp, light] = await Promise.all([
          axios.get("http://127.0.0.1:8000/api/moisture/bound/get/", { headers }), // Độ ẩm
          axios.get("http://127.0.0.1:8000/api/temperature/bound/get/", { headers }), // Nhiệt độ
          axios.get("http://127.0.0.1:8000/api/light/bound/get/", { headers }), // Ánh sáng
        ]);

        setHumidityIndex(humidity)
        setTempIndex(temp)
        setLightIndex(light)

        await Promise.all([
          axios.get("http://127.0.0.1:8000/api/moisture/record/sync/", { headers }),
          axios.get("http://127.0.0.1:8000/api/temperature/record/sync/", { headers }),
          axios.get("http://127.0.0.1:8000/api/light/record/sync/", { headers }),
        ]);

        const [humidityRes, tempRes, lightRes] = await Promise.all([
          axios.get("http://127.0.0.1:8000/api/humidity/record/get/?n=10", { headers }),
          axios.get("http://127.0.0.1:8000/api/temperature/record/get/?n=10", { headers }),
          axios.get("http://127.0.0.1:8000/api/light/record/get/?n=10", { headers }),
        ]);
  
        const formatData = (data) =>
          data.map((item) => ({
            time: new Date(item.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
            value: item.value,
          }));
  
        setHumidityData(formatData(humidityRes.data));
        setTempData(formatData(tempRes.data));
        setLightData(formatData(lightRes.data));
      } catch (err) {
        console.error("Lỗi khi lấy dữ liệu biểu đồ:", err);
      }
    };
  
    fetchData();
  }, [navigate]);

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <div className="flex flex-grow">
        <Sidebar activeItem="overview" />
        <div className="flex-1 p-6">
          <h2 className="text-xl font-bold mb-4">Điều kiện môi trường hiện tại</h2>
          <div className="grid grid-cols-3 gap-6">
            <div className="p-4 bg-white shadow rounded-lg flex items-center">
              <span className="text-2xl mr-2">🌡️</span>
              <div>
                <p className="text-gray-700">Nhiệt độ</p>
                <p className="font-bold">{`${tempIndex}°C`}</p>
              </div>
            </div>
            <div className="p-4 bg-white shadow rounded-lg flex items-center">
              <span className="text-2xl mr-2">☀️</span>
              <div>
                <p className="text-gray-700">Ánh sáng</p>
                <p className="font-bold">{`${lightIndex}%`}</p>
              </div>
            </div>
            <div className="p-4 bg-white shadow rounded-lg flex items-center">
              <span className="text-2xl mr-2">💧</span>
              <div>
                <p className="text-gray-700">Độ ẩm</p>
                <p className="font-bold">{`${humidityIndex}%`}</p>
              </div>
            </div>
          </div>

          <h2 className="text-xl font-bold mt-6">Ảnh chụp cây gần đây nhất</h2>
          <img src={PlantPicture} alt="Cây xanh" className="w-60 h-40 mt-2 rounded shadow" />

          <h2 className="text-xl font-bold mt-6">Thống kê trong 24 giờ qua</h2>
            <div className="grid grid-cols-2 gap-6">
                <ChartComponent title="Biểu đồ nhiệt độ" data={tempData} color="#ff7300" />
                <ChartComponent title="Biểu đồ ánh sáng" data={lightData} color="#fdd835" />
                <ChartComponent title="Biểu đồ độ ẩm" data={humidityData} color="#2196f3" />
            </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default DashboardOverview;
