const PROTO_PATH = './restaurant.proto';

//var grpc = require("grpc");
var grpc = require('@grpc/grpc-js');

var protoLoader = require('@grpc/proto-loader');

const { connectDB } = require('../config/database');
const Menu = require('../models/Menu');

var packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    arrays: true,
});

var restaurantProto = grpc.loadPackageDefinition(packageDefinition);

const { v4: uuidv4 } = require('uuid');

const server = new grpc.Server();

let isDBConnected = false;

const initializeDatabase = async () => {
    try {
        await connectDB();
        isDBConnected = true;
        console.log('database initialized successfully');

        // Seed initial menu data if database is empty
        const menuCount = await Menu.countDocuments();
        if (menuCount === 0) {
            await seedInitialMenu();
            console.log('initial menu data seeded');
        }
    } catch (error) {
        console.error('failed to initialize database:', error);
        isDBConnected = false;
    }
};

const seedInitialMenu = async () => {
    const initialMenu = [
        {
            name: 'Tomyam Gung',
            price: 500,
            description: 'Spicy and sour Thai soup with shrimp',
            category: 'main-course',
        },
        {
            name: 'Somtam',
            price: 60,
            description: 'Fresh papaya salad with spicy dressing',
            category: 'appetizer',
        },
        {
            name: 'Pad-Thai',
            price: 120,
            description: 'Stir-fried rice noodles with eggs and vegetables',
            category: 'main-course',
        },
    ];

    try {
        await Menu.insertMany(initialMenu);
    } catch (error) {
        console.error('Error seeding menu data:', error);
    }
};

server.addService(restaurantProto.RestaurantService.service, {
    getAllMenu: async (_, callback) => {
        const menus = await Menu.find();
        callback(null, { menu: menus });
    },
    get: async (call, callback) => {
        let menuItem = await Menu.findById(call.request.id);

        if (menuItem) {
            callback(null, menuItem);
        } else {
            callback({
                code: grpc.status.NOT_FOUND,
                details: 'Not found',
            });
        }
    },
    insert: async (call, callback) => {
        let menuItem = call.request;

        menuItem.id = uuidv4();
        await menuItem.save();
        callback(null, menuItem);
    },
    update: async (call, callback) => {
        let existingMenuItem = await Menu.findById(call.request.id);

        if (existingMenuItem) {
            existingMenuItem.name = call.request.name;
            existingMenuItem.price = call.request.price;
            await existingMenuItem.save();
            callback(null, existingMenuItem);
        } else {
            callback({
                code: grpc.status.NOT_FOUND,
                details: 'Not Found',
            });
        }
    },
    remove: async (call, callback) => {
        let existingMenuItem = await Menu.findById(call.request.id);

        if (existingMenuItem) {
            await existingMenuItem.deleteOne();
            callback(null, {});
        } else {
            callback({
                code: grpc.status.NOT_FOUND,
                details: 'NOT Found',
            });
        }
    },
});

server.bindAsync('127.0.0.1:30043', grpc.ServerCredentials.createInsecure(), () => {
    server.start();
});
console.log('Server running at http://127.0.0.1:30043');
initializeDatabase();
