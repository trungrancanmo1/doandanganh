import React, { useEffect, useState } from "react";
import Header from "../../components/Header";
import Footer from "../../components/Footer";
import Sidebar from "../../components/Sidebar";
import axiosInstance from "../../components/axiosInstance";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";


const lightHistoryData = [
  { time: "14:00", status: "Bật" },
  { time: "13:00", status: "Tắt" },
  { time: "12:00", status: "Bật" },
  { time: "11:00", status: "Tắt" },
];

const DashboardLightPage = () => {
  const [lightBound, setLightBound] = useState({
    lowest: null,
    highest: null,
  });

  const [editing, setEditing] = useState(false);
  const [editValues, setEditValues] = useState({ lowest: "", highest: "" });
  const [error, setError] = useState(null);

  const [currentLight, setCurrentLight] = useState(null);

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

    const fetchLightBound = async () => {
      try {
        const res = await axiosInstance.get("/light/bound/get/");
        setLightBound({
          lowest: res.data.lowest_allowed,
          highest: res.data.highest_allowed,
        });
      } catch (err) {
        console.error("Lỗi khi tải ngưỡng ánh sáng:", err);
      }
    };

    const fetchCurrentLight = async () => {
      try {
        await axiosInstance.post("/light/record/sync/");
        const res = await axiosInstance.get("/light/record/get/recent/?n=1");
        if (res.data && res.data.length > 0) {
          setCurrentLight(res.data[0].value);
        }
      } catch (err) {
        console.error("Lỗi khi lấy ánh sáng hiện tại:", err);
      }
    };

    fetchLightBound();
    fetchCurrentLight();
  }, [navigate]);

  

  const handleEditClick = () => {
    setEditValues({
      lowest: lightBound.lowest,
      highest: lightBound.highest,
    });
    setEditing(true);
  };

  const handleSave = async () => {
    const lowest = parseFloat(editValues.lowest);
    const highest = parseFloat(editValues.highest);
  
    // Kiểm tra hợp lệ
    if (
      isNaN(lowest) || isNaN(highest) ||
      lowest < 0 || lowest > 100 ||
      highest < 0 || highest > 100
    ) {
      setError({ detail: "Giá trị ánh sáng phải nằm trong khoảng từ 0 đến 100%" });
      return;
    }
  
    try {
      const res = await axiosInstance.patch("/light/bound/update/", {
        lowest_allowed: lowest,
        highest_allowed: highest,
      });
      setLightBound({
        lowest: res.data.lowest_allowed,
        highest: res.data.highest_allowed,
      });
      setEditing(false);
      setError(null);
    } catch (err) {
      console.error("Lỗi khi cập nhật:", err);
      if (err.response?.status === 400) {
        setError(err.response.data);
      } else if (err.response?.status === 405) {
        setError({ detail: err.response.data.detail });
      } else {
        setError({ detail: "Đã xảy ra lỗi không xác định" });
      }
    }
  };
  

  const handleChange = (e) => {
    setEditValues({ ...editValues, [e.target.name]: e.target.value });
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <div className="flex flex-grow">
        <Sidebar activeItem="light" />
        <div className="flex-1 p-6">
          <div className="flex justify-between">
            <div className="w-[60%]">
              <h2 className="text-xl font-bold mb-4">Độ sáng hiện tại</h2>
              <div className="w-48 p-4 bg-white border shadow rounded-lg flex items-center">
                <span className="text-2xl mr-2">☀️</span>
                <div>
                  <p className="text-gray-700">Ánh sáng</p>
                  <p className="font-bold">
                    {currentLight !== null ? `${currentLight} %` : "Đang tải..."}
                  </p>
                </div>
              </div>
            </div>

            {/* Ngưỡng ánh sáng */}
            <div className="w-[40%] pr-6">
              <h2 className="text-xl font-bold mb-4">Mức độ sáng cần thiết</h2>

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
                        {lightBound.lowest !== null
                          ? `${lightBound.lowest} %`
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
                        {lightBound.highest !== null
                          ? `${lightBound.highest} %`
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

              {/* Lỗi */}
              {error && (
                <div className="mt-2 text-red-600 text-sm">
                  {error.detail ||
                    error.lowest_allowed?.[0] ||
                    error.highest_allowed?.[0]}
                </div>
              )}
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

          {/* Điều chỉnh đèn */}
          <h2 className="text-xl font-bold mt-6">Điều chỉnh đèn</h2>
          <div className="w-[20%] bg-white border shadow rounded-lg flex items-center p-4 py-6">
            <label className="inline-flex items-center cursor-pointer">
              <input type="checkbox" value="" className="sr-only peer" />
              <div className="relative w-11 h-6 bg-gray-400 peer-focus:outline-none peer-focus:ring-1 peer-focus:ring-gray-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
              <span className="ms-3 text-sm font-bold">Bật</span>
            </label>
          </div>

          {/* Lịch sử bật/tắt đèn */}
          <h2 className="text-xl font-bold mt-6 mb-2">Lịch sử bật, tắt đèn</h2>
          <div className="w-[60%] border shadow rounded-lg bg-white">
            {lightHistoryData.map((item, index) => (
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

export default DashboardLightPage;
