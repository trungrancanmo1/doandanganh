import React, { useEffect, useRef, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import Sidebar from "../components/Sidebar";
import axiosInstance from "../components/axiosInstance";
import PlantPicture from "../assets/plantPicture.jpg";
import { jwtDecode } from "jwt-decode";

const ChartComponent = ({ title, data, color }) => (
    <div className="p-4 bg-white shadow rounded-lg">
        <h3 className="font-bold mb-2">{title}</h3>
        <ResponsiveContainer width="100%" height={200}>
            <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" reversed />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke={color} strokeWidth={2} />
            </LineChart>
        </ResponsiveContainer>
    </div>
);

const DashboardOverview = () => {
    const navigate = useNavigate();
    const socketRef = useRef(null);

    const [humidityIndex, setHumidityIndex] = useState([]);
    const [tempIndex, setTempIndex] = useState([]);
    const [lightIndex, setLightIndex] = useState([]);

    const [humidityData, setHumidityData] = useState([]);
    const [tempData, setTempData] = useState([]);
    const [lightData, setLightData] = useState([]);

    useEffect(() => {
        const token = localStorage.getItem("access_token");

        if (!token) {
            navigate("/login");
            return;
        }

        let decoded;
        try {
            decoded = jwtDecode(token);
            const now = Date.now() / 1000;
            if (decoded.exp < now) {
                navigate("/login");
                return;
            }
        } catch (err) {
            console.error("Token không hợp lệ:", err);
            navigate("/login");
            return;
        }

        // Get historical data for charts
        const fetchChartData = async () => {
            try {
                const [humidityRes, tempRes, lightRes] = await Promise.all([
                    axiosInstance.get("/moisture/record/get/recent/?n=20"),
                    axiosInstance.get("/temperature/record/get/recent/?n=20"),
                    axiosInstance.get("/light/record/get/recent/?n=20"),
                ]);

                const formatData = (data) =>
                    data.map((item) => {
                        const date = new Date(item.timestamp);
                        date.setHours(date.getHours() + 7);
                        const time = date.toLocaleTimeString([], {
                            hour: "2-digit",
                            minute: "2-digit",
                        });

                        return {
                            time,
                            value: item.value,
                        };
                    });

                setHumidityData(formatData(humidityRes.data));
                setTempData(formatData(tempRes.data));
                setLightData(formatData(lightRes.data));
            } catch (error) {
                console.error("Lỗi khi lấy dữ liệu biểu đồ:", error);
            }
        };

        fetchChartData();

        // Open WebSocket connection for real-time updates
        const ws = new WebSocket(`ws://localhost:8080/ws?token=${token}`);

        ws.onopen = () => {
            console.log("WebSocket connected");
        };

        ws.onmessage = (event) => {
          try {
              const data = JSON.parse(event.data);
      
              const now = new Date();
              now.setHours(now.getHours() + 7);
              const time = now.toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
              });
      
              if (data.type === "temperature") {
                  setTempIndex([{ value: data.value, time }]);
              } else if (data.type === "humidity") {
                  setHumidityIndex([{ value: data.value, time }]);
              } else if (data.type === "light") {
                  setLightIndex([{ value: data.value, time }]);
              } else {
                  console.warn("Không xác định loại dữ liệu:", data.type);
              }
          } catch (err) {
              console.error("Lỗi phân tích WebSocket message:", err);
          }
      };
      

        ws.onerror = (err) => {
            console.error("WebSocket error:", err);
        };

        ws.onclose = () => {
            console.warn("WebSocket closed");
        };

        socketRef.current = ws;

        return () => {
            ws.close();
        };
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
                                <p className="font-bold">
                                    {tempIndex.length > 0 ? `${tempIndex[0].value}°C` : "Đang tải..."}
                                </p>
                            </div>
                        </div>
                        <div className="p-4 bg-white shadow rounded-lg flex items-center">
                            <span className="text-2xl mr-2">☀️</span>
                            <div>
                                <p className="text-gray-700">Ánh sáng</p>
                                <p className="font-bold">
                                    {lightIndex.length > 0 ? `${lightIndex[0].value}%` : "Đang tải..."}
                                </p>
                            </div>
                        </div>
                        <div className="p-4 bg-white shadow rounded-lg flex items-center">
                            <span className="text-2xl mr-2">💧</span>
                            <div>
                                <p className="text-gray-700">Độ ẩm</p>
                                <p className="font-bold">
                                    {humidityIndex.length > 0 ? `${humidityIndex[0].value}%` : "Đang tải..."}
                                </p>
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
