{
    "name": "Hotel Manager",
    "version": "17.0.1.0.0",
    "summary": "Quản lý khách sạn: phòng, khách, booking, dịch vụ",
    "depends": ["base"],
    "data": [
        "security/hotel_security.xml",
        "security/ir.model.access.csv",
        "views/hotel_menus.xml",
        "views/hotel_room_type_views.xml",
        "views/hotel_service_views.xml",
        "views/hotel_customer_views.xml",
        "views/hotel_booking_views.xml",
        "views/hotel_room_views.xml",
    ],
    "installable": True,
    "application": True,
}
