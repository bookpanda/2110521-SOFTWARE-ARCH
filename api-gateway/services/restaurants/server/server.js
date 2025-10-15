require('dotenv').config();

const PROTO_PATH="./restaurant.proto";

//var grpc = require("grpc");
var grpc = require("@grpc/grpc-js");
const mongoose = require("mongoose");
const Menu = require("./models/Menu");

var protoLoader = require("@grpc/proto-loader");

var packageDefinition = protoLoader.loadSync(PROTO_PATH,{
    keepCase: true,
    longs: String,
    enums: String,
    arrays: true
});

var restaurantProto =grpc.loadPackageDefinition(packageDefinition);

const {v4: uuidv4}=require("uuid");

mongoose.connect(process.env.MONGODB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

mongoose.connection.on('connected', () => {
    console.log('Connected to MongoDB:', process.env.MONGODB_URI);
});

mongoose.connection.on('error', (err) => {
    console.error('MongoDB connection error:', err);
});

const server = new grpc.Server();

server.addService(restaurantProto.RestaurantService.service,{
    getAllMenu: async (_,callback)=>{
        try {
            const menu = await Menu.find({});
            callback(null, {menu});
        } catch (error) {
            callback({
                code: grpc.status.INTERNAL,
                details: error.message
            });
        }
    },
    get: async (call,callback)=>{
        try {
            const menuItem = await Menu.findOne({id: call.request.id});

            if(menuItem) {
                callback(null, {
                    id: menuItem.id,
                    name: menuItem.name,
                    price: menuItem.price
                });
            } else {
                callback({
                    code: grpc.status.NOT_FOUND,
                    details: "Not found"
                });
            }
        } catch (error) {
            callback({
                code: grpc.status.INTERNAL,
                details: error.message
            });
        }
    },
    insert: async (call, callback)=>{
        try {
            const menuItem = {
                id: uuidv4(),
                name: call.request.name,
                price: call.request.price
            };

            const newMenuItem = new Menu(menuItem);
            await newMenuItem.save();
            
            callback(null, {
                id: newMenuItem.id,
                name: newMenuItem.name,
                price: newMenuItem.price
            });
        } catch (error) {
            callback({
                code: grpc.status.INTERNAL,
                details: error.message
            });
        }
    },
    update: async (call,callback)=>{
        try {
            const updatedMenuItem = await Menu.findOneAndUpdate(
                {id: call.request.id},
                {
                    name: call.request.name,
                    price: call.request.price
                },
                {new: true}
            );

            if(updatedMenuItem) {
                callback(null, {
                    id: updatedMenuItem.id,
                    name: updatedMenuItem.name,
                    price: updatedMenuItem.price
                });
            } else {
                callback({
                    code: grpc.status.NOT_FOUND,
                    details: "Not Found"
                });
            }
        } catch (error) {
            callback({
                code: grpc.status.INTERNAL,
                details: error.message
            });
        }
    },
    remove: async (call, callback) => {
        try {
            const deletedMenuItem = await Menu.findOneAndDelete({id: call.request.id});

            if(deletedMenuItem) {
                callback(null, {});
            } else {
                callback({
                    code: grpc.status.NOT_FOUND,
                    details: "Not Found"
                });
            }
        } catch (error) {
            callback({
                code: grpc.status.INTERNAL,
                details: error.message
            });
        }
    }
});

const port = process.env.PORT || 30043;
server.bindAsync(`0.0.0.0:${port}`,grpc.ServerCredentials.createInsecure(), ()=>{server.start();});
console.log(`Server running at http://0.0.0.0:${port}`);
