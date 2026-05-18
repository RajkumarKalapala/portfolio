const Wishlist = require("../models/Wishlist")

exports.create = async (req, res) => {
    try {

        const created = new Wishlist(req.body)

        await created.save()

        const populatedWishlist = await Wishlist.findById(created._id)
            .populate({
                path: "product",
                populate: ["brand"]
            })

        // Product might be deleted
        if (!populatedWishlist.product) {
            await Wishlist.findByIdAndDelete(created._id)

            return res.status(404).json({
                message: "Product no longer exists"
            })
        }

        res.status(201).json(populatedWishlist)

    } catch (error) {
        console.log(error)

        res.status(500).json({
            message: "Error adding product to wishlist, please try again later"
        })
    }
}

exports.getByUserId = async (req, res) => {

    try {

        const { id } = req.params

        let skip = 0
        let limit = 0

        if (req.query.page && req.query.limit) {

            const pageSize = Number(req.query.limit)
            const page = Number(req.query.page)

            skip = pageSize * (page - 1)
            limit = pageSize
        }

        let result = await Wishlist.find({ user: id })
            .skip(skip)
            .limit(limit)
            .populate({
                path: "product",
                populate: ["brand"]
            })

        // REMOVE BROKEN PRODUCTS
        result = result.filter(item => item.product)

        const totalResults = result.length

        res.set("X-Total-Count", totalResults)

        res.status(200).json(result)

    } catch (error) {

        console.log(error)

        res.status(500).json({
            message: "Error fetching your wishlist, please try again later"
        })
    }
}

exports.updateById = async (req, res) => {

    try {

        const { id } = req.params

        const updated = await Wishlist.findByIdAndUpdate(
            id,
            req.body,
            { new: true }
        ).populate({
            path: "product",
            populate: ["brand"]
        })

        // Handle deleted product
        if (updated && !updated.product) {

            await Wishlist.findByIdAndDelete(id)

            return res.status(404).json({
                message: "Product no longer exists"
            })
        }

        res.status(200).json(updated)

    } catch (error) {

        console.log(error)

        res.status(500).json({
            message: "Error updating your wishlist, please try again later"
        })
    }
}

exports.deleteById = async (req, res) => {

    try {

        const { id } = req.params

        const deleted = await Wishlist.findByIdAndDelete(id)

        return res.status(200).json(deleted)

    } catch (error) {

        console.log(error)

        res.status(500).json({
            message: "Error deleting that product from wishlist, please try again later"
        })
    }
}
