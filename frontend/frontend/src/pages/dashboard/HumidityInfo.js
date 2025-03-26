import React, { useEffect, useState } from "react";
import Header from "../../components/Header";
import Footer from "../../components/Footer";
import Sidebar from "../../components/Sidebar";
import axiosInstance from "../../components/axiosInstance";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

// Dữ liệu mẫu cho lịch sử máy bơm
const pumpHistoryData = [
  { time: "14:30", status: "Bật" },
  { time: "13:10", status: "Tắt" },
  { time: "12:45", status: "Bật" },
  { time: "11:20", status: "Tắt" },
  { time: "11:20", status: "Tắt" },
  { time: "11:20", status: "Tắt" },
  { time: "11:20", status: "Tắt" },
];

const DashboardHumidityPage = () => {

  const [moistureBound, setMoistureBound] = useState({ lowest: null, highest: null });
  const [editing, setEditing] = useState(false);
  const [editValues, setEditValues] = useState({ lowest: "", highest: "" });
  const [currentMoisture, setCurrentMoisture] = useState(null);
  const navigate = useNavigate();

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
  
    const fetchMoistureBound = async () => {
      try {
        const res = await axiosInstance.get("/moisture/bound/get/");
        setMoistureBound({
          lowest: res.data.lowest_allowed,
          highest: res.data.highest_allowed,
        });
      } catch (err) {
        console.error("Lỗi khi tải ngưỡng độ ẩm:", err);
      }
    };
  
    const fetchCurrentMoisture = async () => {
      try {
        await axiosInstance.post("/moisture/record/sync/");
        const res = await axiosInstance.get("/moisture/record/get/recent/?n=1");
        if (res.data && res.data.length > 0) {
          setCurrentMoisture(res.data[0].value);
        }
      } catch (err) {
        console.error("Lỗi khi lấy độ ẩm hiện tại:", err);
      }
    };
  
    fetchMoistureBound();
    fetchCurrentMoisture();
  }, [navigate]);
  

  const handleEditClick = () => {
    setEditValues({
      lowest: moistureBound.lowest,
      highest: moistureBound.highest,
    });
    setEditing(true);
  };
  
  const handleSave = async () => {
    const lowest = parseFloat(editValues.lowest);
    const highest = parseFloat(editValues.highest);
  
    try {
      const res = await axiosInstance.patch("/moisture/bound/update/", {
        lowest_allowed: lowest,
        highest_allowed: highest,
      });
  
      setMoistureBound({
        lowest: res.data.lowest_allowed,
        highest: res.data.highest_allowed,
      });
  
      setEditing(false);
    } catch (err) {
      console.error("Lỗi khi cập nhật:", err);
    }
  };
  

  const handleChange = (e) => {
    setEditValues({ ...editValues, [e.target.name]: e.target.value });
  };


  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <div className="flex flex-grow">
        <Sidebar activeItem="humidity" />
        <div className="flex-1 p-6">
          <div className="flex justify-between">
            <div className="w-[60%]">
              <h2 className="text-xl font-bold mb-4">Độ ẩm hiện tại</h2>
              <div className="w-48 p-4 bg-white border shadow rounded-lg flex items-center">
                <span className="text-2xl mr-2">💧</span>
                <div>
                  <p className="text-gray-700">Độ ẩm</p>
                  <p className="font-bold">
                    {currentMoisture !== null ? `${currentMoisture}%` : "Đang tải..."}
                  </p>
                </div>
              </div>
            </div>
            <div className="w-[40%] pr-6">
              <h2 className="text-xl font-bold mb-4">Ngưỡng độ ẩm cần thiết</h2>
              <div
                className={`grid grid-rows-2 gap-y-2 p-4 border shadow rounded-lg items-center font-bold ${
                  editing ? "bg-yellow-50 border-yellow-500" : "bg-white"
                }`}
              >
                {/* HÀNG TỪ */}
                <div className="flex justify-between items-center">
                  <div className="w-[18%]">Từ</div>
                  <div className="flex-grow mx-1">
                    {editing ? (
                      <div className="border border-yellow-500 rounded px-2 py-1 bg-white">
                        <input
                          type="number"
                          name="lowest"
                          value={editValues.lowest}
                          onChange={handleChange}
                          className="w-full outline-none"
                        />
                      </div>
                    ) : (
                      <div className="bg-gray-300 rounded-sm text-center py-1">
                        {moistureBound.lowest !== null
                          ? `${moistureBound.lowest} %`
                          : "Đang tải..."}
                      </div>
                    )}
                  </div>
                  <div className="w-[26%]"></div>
                </div>

                {/* HÀNG ĐẾN */}
                <div className="flex justify-between items-center">
                  <div className="w-[18%]">Đến</div>
                  <div className="flex-grow mx-1">
                    {editing ? (
                      <div className="border border-yellow-500 rounded px-2 py-1 bg-white">
                        <input
                          type="number"
                          name="highest"
                          value={editValues.highest}
                          onChange={handleChange}
                          className="w-full outline-none"
                        />
                      </div>
                    ) : (
                      <div className="bg-gray-300 rounded-sm text-center py-1">
                        {moistureBound.highest !== null
                          ? `${moistureBound.highest} %`
                          : "Đang tải..."}
                      </div>
                    )}
                  </div>
                  <div className="w-[26%] flex justify-end space-x-2">
                    {editing ? (
                      <>
                        <button
                          className="bg-green-600 text-white text-xs rounded-md px-2 hover:bg-green-700"
                          onClick={handleSave}
                        >
                          Lưu
                        </button>
                        <button
                          className="bg-gray-400 text-white text-xs rounded-md px-2 hover:bg-gray-500"
                          onClick={() => setEditing(false)}
                        >
                          Hủy
                        </button>
                      </>
                    ) : (
                      <button
                        className="bg-[#598868] text-white text-xs hover:bg-green-600 rounded-md px-2"
                        onClick={handleEditClick}
                      >
                        Chỉnh sửa
                      </button>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Chế độ điều chỉnh */}
          <h2 className="text-xl font-bold mt-6">Chế độ điều chỉnh</h2>
          <div className="grid grid-cols-2 gap-x-2 w-[50%] font-bold">
            <div className="p-4 py-6 bg-white border shadow rounded-lg flex items-center">
              <input type="radio" name="light-mode" className="mr-2" />
              <p>Thủ công</p>
            </div>
            <div className="p-4 py-6 bg-white border shadow rounded-lg flex items-center">
              <input type="radio" name="light-mode" className="mr-2" />
              <p>Tự động</p>
            </div>
          </div>

          {/* Điều chỉnh bơm nước */}
          <h2 className="text-xl font-bold mt-6">Điều chỉnh bơm nước</h2>
          <div className="w-48 bg-white border shadow rounded-lg flex items-center p-4 py-6">
            <label className="inline-flex items-center cursor-pointer">
              <input type="checkbox" value="" className="sr-only peer" />
              <div className="relative w-11 h-6 bg-gray-400 peer-focus:outline-none peer-focus:ring-1 peer-focus:ring-gray-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
              <span className="ms-3 text-sm font-bold">Bật</span>
            </label>
          </div>

          {/* Lịch sử hoạt động máy bơm */}
          <h2 className="text-xl font-bold mt-6 mb-2">Lịch sử hoạt động máy bơm</h2>
          <div className="w-[60%] border shadow rounded-lg bg-white">
            {pumpHistoryData.map((item, index) => (
              <div
                key={index}
                className="flex items-center px-4 py-3 border-b last:border-none"
              >
                <span className="mr-2 pl-2">🕒</span>
                <span className="text-gray-500 text-sm w-[20%]">{item.time}</span>
                <span
                  className={`ml-auto font-semibold ${
                    item.status === "Bật" ? "text-green-600" : "text-red-600"
                  }`}
                >
                  {item.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default DashboardHumidityPage;
