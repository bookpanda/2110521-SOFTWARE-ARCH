const mongoose = require('mongoose');

const menuSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Menu item name is required'],
    trim: true,
    maxlength: [100, 'Menu item name cannot exceed 100 characters']
  },
  price: {
    type: Number,
    required: [true, 'Price is required'],
    min: [0, 'Price cannot be negative'],
    validate: {
      validator: function(v) {
        return v >= 0;
      },
      message: 'Price must be a positive number'
    }
  },
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

menuSchema.index({ name: 1 });

menuSchema.methods.updatePrice = function(newPrice) {
  if (newPrice < 0) {
    throw new Error('Price cannot be negative');
  }
  this.price = newPrice;
  return this.save();
};

menuSchema.pre('save', function(next) {
  if (this.price < 0) {
    next(new Error('Price cannot be negative'));
  }
  next();
});

const Menu = mongoose.model('Menu', menuSchema);

module.exports = Menu;
