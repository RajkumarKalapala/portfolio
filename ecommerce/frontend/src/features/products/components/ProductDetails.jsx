import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate, useParams } from 'react-router-dom'

import {
  clearSelectedProduct,
  fetchProductByIdAsync,
  resetProductFetchStatus,
  selectProductFetchStatus,
  selectSelectedProduct
} from '../ProductSlice'

import {
  Box,
  Checkbox,
  Rating,
  Stack,
  Typography,
  useMediaQuery,
  Button
} from '@mui/material'

import {
  addToCartAsync,
  resetCartItemAddStatus,
  selectCartItemAddStatus,
  selectCartItems
} from '../../cart/CartSlice'

import { selectLoggedInUser } from '../../auth/AuthSlice'

import {
  fetchReviewsByProductIdAsync,
  resetReviewFetchStatus,
  selectReviewFetchStatus,
  selectReviews,
} from '../../review/ReviewSlice'

import { Reviews } from '../../review/components/Reviews'

import { toast } from 'react-toastify'

import { MotionConfig, motion } from 'framer-motion'

import FavoriteBorder from '@mui/icons-material/FavoriteBorder'
import Favorite from '@mui/icons-material/Favorite'

import LocalShippingOutlinedIcon from '@mui/icons-material/LocalShippingOutlined'
import CachedOutlinedIcon from '@mui/icons-material/CachedOutlined'

import {
  createWishlistItemAsync,
  deleteWishlistItemByIdAsync,
  resetWishlistItemAddStatus,
  resetWishlistItemDeleteStatus,
  selectWishlistItemAddStatus,
  selectWishlistItemDeleteStatus,
  selectWishlistItems
} from '../../wishlist/WishlistSlice'

import { useTheme } from '@mui/material'

import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft'
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight'

import SwipeableViews from 'react-swipeable-views'
import { autoPlay } from 'react-swipeable-views-utils'

import MobileStepper from '@mui/material/MobileStepper'

import Lottie from 'lottie-react'

import { loadingAnimation } from '../../../assets'

const SIZES = ['XS', 'S', 'M', 'L', 'XL']

const COLORS = [
  '#020202',
  '#F6F6F6',
  '#B82222',
  '#BEA9A9',
  '#E2BB8D'
]

const AutoPlaySwipeableViews = autoPlay(SwipeableViews)

export const ProductDetails = () => {

  const { id } = useParams()

  const product = useSelector(selectSelectedProduct)

  const loggedInUser = useSelector(selectLoggedInUser)

  const dispatch = useDispatch()

  const cartItems = useSelector(selectCartItems)

  const cartItemAddStatus = useSelector(selectCartItemAddStatus)

  const [quantity, setQuantity] = useState(1)

  const [selectedSize, setSelectedSize] = useState('')

  const [selectedColorIndex, setSelectedColorIndex] = useState(-1)

  const reviews = useSelector(selectReviews)

  const [selectedImageIndex, setSelectedImageIndex] = useState(0)

  const theme = useTheme()

  const is1420 = useMediaQuery(theme.breakpoints.down(1420))
  const is990 = useMediaQuery(theme.breakpoints.down(990))
  const is840 = useMediaQuery(theme.breakpoints.down(840))
  const is500 = useMediaQuery(theme.breakpoints.down(500))
  const is480 = useMediaQuery(theme.breakpoints.down(480))
  const is387 = useMediaQuery(theme.breakpoints.down(387))
  const is340 = useMediaQuery(theme.breakpoints.down(340))

  const wishlistItems = useSelector(selectWishlistItems)

  // SAFE checks
  const isProductAlreadyInCart = cartItems.some(
    (item) => item?.product?._id === id
  )

  const isProductAlreadyinWishlist = wishlistItems.some(
    (item) => item?.product?._id === id
  )

  const productFetchStatus = useSelector(selectProductFetchStatus)

  const reviewFetchStatus = useSelector(selectReviewFetchStatus)

  const totalReviewRating = reviews.reduce(
    (acc, review) => acc + review.rating,
    0
  )

  const totalReviews = reviews.length

  const averageRating = parseInt(
    Math.ceil(totalReviewRating / totalReviews)
  )

  const wishlistItemAddStatus = useSelector(selectWishlistItemAddStatus)

  const wishlistItemDeleteStatus = useSelector(selectWishlistItemDeleteStatus)

  const navigate = useNavigate()

  useEffect(() => {
    window.scrollTo({
      top: 0,
      behavior: "instant"
    })
  }, [])

  useEffect(() => {

    if (id) {
      dispatch(fetchProductByIdAsync(id))
      dispatch(fetchReviewsByProductIdAsync(id))
    }

  }, [id])

  useEffect(() => {

    if (cartItemAddStatus === 'fulfilled') {
      toast.success("Product added to cart")
    }

    else if (cartItemAddStatus === 'rejected') {
      toast.error('Error adding product to cart, please try again later')
    }

  }, [cartItemAddStatus])

  useEffect(() => {

    if (wishlistItemAddStatus === 'fulfilled') {
      toast.success("Product added to wishlist")
    }

    else if (wishlistItemAddStatus === 'rejected') {
      toast.error("Error adding product to wishlist, please try again later")
    }

  }, [wishlistItemAddStatus])

  useEffect(() => {

    if (wishlistItemDeleteStatus === 'fulfilled') {
      toast.success("Product removed from wishlist")
    }

    else if (wishlistItemDeleteStatus === 'rejected') {
      toast.error("Error removing product from wishlist, please try again later")
    }

  }, [wishlistItemDeleteStatus])

  useEffect(() => {

    if (productFetchStatus === 'rejected') {
      toast.error("Error fetching product details, please try again later")
    }

  }, [productFetchStatus])

  useEffect(() => {

    if (reviewFetchStatus === 'rejected') {
      toast.error("Error fetching product reviews, please try again later")
    }

  }, [reviewFetchStatus])

  useEffect(() => {

    return () => {

      dispatch(clearSelectedProduct())
      dispatch(resetProductFetchStatus())
      dispatch(resetReviewFetchStatus())
      dispatch(resetWishlistItemDeleteStatus())
      dispatch(resetWishlistItemAddStatus())
      dispatch(resetCartItemAddStatus())

    }

  }, [])

  const handleAddToCart = () => {

    const item = {
      user: loggedInUser?._id,
      product: id,
      quantity
    }

    dispatch(addToCartAsync(item))

    setQuantity(1)
  }

  const handleDecreaseQty = () => {

    if (quantity !== 1) {
      setQuantity(quantity - 1)
    }

  }

  const handleIncreaseQty = () => {

    if (quantity < 20 && quantity < product?.stockQuantity) {
      setQuantity(quantity + 1)
    }

  }

  const handleSizeSelect = (size) => {
    setSelectedSize(size)
  }

  const handleAddRemoveFromWishlist = (e) => {

    if (e.target.checked) {

      const data = {
        user: loggedInUser?._id,
        product: id
      }

      dispatch(createWishlistItemAsync(data))
    }

    else if (!e.target.checked) {

      const index = wishlistItems.findIndex(
        (item) => item?.product?._id === id
      )

      if (index !== -1) {
        dispatch(deleteWishlistItemByIdAsync(wishlistItems[index]._id))
      }
    }
  }

  const [activeStep, setActiveStep] = React.useState(0)

  const maxSteps = product?.images?.length || 0

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1)
  }

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1)
  }

  const handleStepChange = (step) => {
    setActiveStep(step)
  }

  return (
    <>
      {/* Your remaining JSX stays SAME */}
    </>
  )
}
