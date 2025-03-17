import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Header from "../components/Header";
import Footer from "../components/Footer";
import PlantPicture from "../assets/plantPicture.jpg";

const ImageModal = ({ selectedImage, setSelectedImage }) => {
    return (
        <AnimatePresence>
            {selectedImage && (
                <motion.div
                    className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
                    onClick={() => setSelectedImage(null)}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                >
                    <motion.div
                        className="bg-white p-4 rounded-lg shadow-lg"
                        initial={{ scale: 0.8 }}
                        animate={{ scale: 1 }}
                        exit={{ scale: 0.8 }}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <img
                            src={selectedImage}
                            alt="Ảnh chi tiết"
                            className="rounded-md"
                        />
                        <button
                            className="mt-2 px-4 py-2 bg-red-500 text-white rounded-md w-full"
                            onClick={() => setSelectedImage(null)}
                        >
                            Đóng
                        </button>
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

const DiseaseStatus = () => {
    const historyData = [
        { time: "13:00", status: "Không phát hiện sâu bệnh", detected: false },
        { time: "12:00", status: "Không phát hiện sâu bệnh", detected: false },
        { time: "11:00", status: "Không phát hiện sâu bệnh", detected: false },
        { time: "10:00", status: "Phát hiện sâu bệnh", detected: true },
        { time: "09:00", status: "Không phát hiện sâu bệnh", detected: false },
    ];

    const [selectedImage, setSelectedImage] = useState(null);

    return (
        <div className="flex flex-col min-h-screen">
            <Header />
            <div className="flex flex-grow">
                <div className="w-1/6 bg-[#598868] text-white p-2">
                    <ul className="w-full">
                        <li className="py-3 pl-4 hover:bg-green-600 cursor-pointer rounded-lg">Thông báo chung</li>
                        <li className="py-3 pl-4 hover:bg-green-600 cursor-pointer rounded-lg">Tổng quan thông số</li>
                        <li className="py-3 pl-4 hover:bg-green-600 cursor-pointer rounded-lg">Ánh sáng</li>
                        <li className="py-3 pl-4 hover:bg-green-600 cursor-pointer rounded-lg">Nhiệt độ</li>
                        <li className="py-3 pl-4 hover:bg-green-600 cursor-pointer rounded-lg">Độ ẩm</li>
                        <li className="py-3 pl-4 bg-gray-300 text-black rounded-lg">Tình trạng sâu bệnh</li>
                    </ul>
                </div>
                <div className="flex-grow p-6">
                    <div className="flex justify-between items-start mb-6">
                        <div className="w-2/3 pr-4">
                            <h2 className="text-xl font-semibold mb-2">Ảnh chụp cây gần đây nhất</h2>
                            <div className="border rounded-lg shadow-md p-2 bg-white">
                                <img
                                    src={PlantPicture}
                                    alt="Cây gần nhất"
                                    className="w-full max-w-md rounded-lg cursor-pointer hover:scale-105 transition-transform"
                                    onClick={() => setSelectedImage(PlantPicture)}
                                />
                            </div>
                        </div>
                        <div className="w-1/3">
                            <h2 className="text-xl font-semibold mb-2">Thông báo</h2>
                            <div className="p-4 border rounded-lg shadow-md bg-white">
                                <div className="flex items-center border rounded-lg p-3 shadow-sm">
                                    <span className="text-2xl pl-4">🕒</span>
                                    <div className="flex flex-col ml-3">
                                        <span className="text-gray-700 font-medium">Thời gian chụp</span>
                                        <span className="text-lg font-bold text-black">14:00</span>
                                    </div>
                                </div>
                                <div className="mt-3 px-4 py-2 bg-green-100 text-green-700 font-semibold text-center rounded-md">
                                    Không phát hiện sâu bệnh
                                </div>
                            </div>
                        </div>
                    </div>
                    <div>
                        <h2 className="text-xl font-semibold mb-2">Lịch sử phân tích trong 24 giờ qua</h2>
                        <div className="border rounded-lg shadow-md bg-white">
                            {historyData.map((item, index) => (
                                <div key={index} className="flex items-center px-4 py-2 border-b last:border-none">
                                    <img
                                        src={PlantPicture}
                                        alt="Ảnh lịch sử"
                                        className="w-10 h-10 rounded-md mr-3 cursor-pointer hover:scale-110 transition-transform"
                                        onClick={() => setSelectedImage(PlantPicture)}
                                    />
                                    <span className="mr-2 pl-20">🕒</span>
                                    <span className="text-gray-700">{item.time}</span>
                                    <span
                                        className={`ml-auto font-semibold ${
                                            item.detected ? "text-red-600" : "text-green-600"
                                        }`}
                                    >
                                        {item.status}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
            <ImageModal selectedImage={selectedImage} setSelectedImage={setSelectedImage} />
            <Footer />
        </div>
    );
};

export default DiseaseStatus;
