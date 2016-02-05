# PLANS

## 1: Get a solid bulid strategy

It would be very helpful to consolidate all of the build process for an entire
deployment of motes: both border router *and* the deployed motes. There are several parts
to this (in no real order):

- change sload so that it has a separate cache for each mote ID. This is to
  prevent a cascading cache invalidation that occurs when we flash all of the
  motes in some order, and should hopefully speed up the programming process by
  a fair amount
- Augment the YAML configuration file. We really want this to do a collection of things:
    - build flags on a per-mote basis
    - we also want 'collections' of build-flags for certain classes of motes -- most obviously border router and normal mote
        ```cfg
        # flags example

        [globalflags]
        RF230_DEF_CHANNEL=24
        KERNEL_STFU = false
        BLIP_STFU = false

        [flags:border_router]
        RPL_SINGLE_HOP_ROOT = true # defines this
        RPL_SINGLE_HOP = false # does *not* define this
        BLIP_ADDR_AUTOCONF = 0 # assigns value to variable
        BLIP_SEND_ROUTER_SOLICITATIONS = 0
        BLIP_SEND_ROUTER_ADVERTISEMENTS = 1
        WITH_WIZ = true
        BORDER_ROUTER = true
        LINKERFILE = stormkernel_ethshield.ld

        [flags:mote]
        BLIP_ADDR_AUTOCONF=1
        BLIP_SEND_ROUTER_SOLICITATIONS=1
        BLIP_SEND_ROUTER_ADVERTISEMENTS=0

        # mote example
        [mote:4014]
        flags = mote
        ignore = 4015, 400f
        isroot = false

        [mote:400f]
        flags = border_router
        ignore = 4014
        isroot = true
        ```
