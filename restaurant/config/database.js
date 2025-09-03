const mongoose = require('mongoose');
require('dotenv').config();

const dbConfig = {
    uri: process.env.MONGODB_URI,
    options: {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        serverSelectionTimeoutMS: 5000,
        socketTimeoutMS: 45000,
    },
};

const connectDB = async () => {
    try {
        const conn = await mongoose.connect(dbConfig.uri, dbConfig.options);

        console.log(`mongodb connected: ${conn.connection.host}:${conn.connection.port}`);

        mongoose.connection.on('error', (err) => {
            console.error('mongodb connection error:', err);
        });

        mongoose.connection.on('disconnected', () => {
            console.log('mongodb disconnected');
        });

        mongoose.connection.on('reconnected', () => {
            console.log('mongodb reconnected');
        });

        // Graceful shutdown
        process.on('SIGINT', async () => {
            try {
                await mongoose.connection.close();
                console.log('mongodb connection closed through app termination');
            } catch (err) {
                console.error('Error during mongodb connection closure:', err);
            }
        });

        return conn;
    } catch (error) {
        console.error('mongodb connection failed:', error.message);
    }
};

const getDBStatus = () => {
    return {
        readyState: mongoose.connection.readyState,
        host: mongoose.connection.host,
        port: mongoose.connection.port,
        name: mongoose.connection.name,
        isConnected: mongoose.connection.readyState === 1,
    };
};

module.exports = {
    connectDB,
    getDBStatus,
    dbConfig,
};
