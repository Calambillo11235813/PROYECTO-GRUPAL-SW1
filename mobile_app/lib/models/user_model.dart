/// Modelo de Usuario
class User {
  final int? id;
  final String email;
  final String username;
  final String firstName;
  final String lastName;
  final bool? isVerified;
  final DateTime? createdAt;

  User({
    this.id,
    required this.email,
    required this.username,
    required this.firstName,
    required this.lastName,
    this.isVerified,
    this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      username: json['username'],
      firstName: json['first_name'],
      lastName: json['last_name'],
      isVerified: json['is_verified'],
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'])
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'username': username,
      'first_name': firstName,
      'last_name': lastName,
      'is_verified': isVerified,
      'created_at': createdAt?.toIso8601String(),
    };
  }

  String get fullName => '$firstName $lastName';
}
