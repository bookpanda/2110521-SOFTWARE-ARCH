const PROTO_PATH="./restaurant.proto";

const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");

var packageDefinition = protoLoader.loadSync(PROTO_PATH,{
    keepCase: true,
    longs: String,
    enums: String,
    arrays: true
});

var restaurantService =grpc.loadPackageDefinition(packageDefinition).RestaurantService;

// Use Kong gRPC gateway instead of direct connection
const SERVICE_API_URL = process.env.SERVICE_API_URL || "kong:8000";
const client = new restaurantService(SERVICE_API_URL, grpc.credentials.createInsecure());

module.exports = client;